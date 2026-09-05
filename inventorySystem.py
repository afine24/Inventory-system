import sys
sys.path.append(".venv/lib/python3.12/site-packages/")
sys.path.append("./lib")
from usb import core
from usb import util
import logger
import requests
import LCD_handler
import DBhandler
import RPi.GPIO as GPIO


email = 'jm85nhsxzc@privaterelay.appleid.com' # PUT YOUR EMAIL HERE
                                              # doing this will allow OpenFoodFacts to contact you if they need to

L1 = 25
L2 = 8
L3 = 7
L4 = 1

C1 = 12
C2 = 16
C3 = 20
C4 = 21
try:
    GPIO.cleanup()
except Exception:
    pass
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)




GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Make sure to configure the input pins to use the internal pull-down resistors

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def hid2ascii(lst):
    """The USB HID device sends an 8-byte code for every character. This
    routine converts the HID code to an ASCII character.
    
    See https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf
    for a complete code table. Only relevant codes are used here."""
    
    # Example input from scanner representing the string "http:":
    #   array('B', [0, 0, 11, 0, 0, 0, 0, 0])   # h
    #   array('B', [0, 0, 23, 0, 0, 0, 0, 0])   # t
    #   array('B', [0, 0, 0, 0, 0, 0, 0, 0])    # nothing, ignore
    #   array('B', [0, 0, 23, 0, 0, 0, 0, 0])   # t
    #   array('B', [0, 0, 19, 0, 0, 0, 0, 0])   # p
    #   array('B', [2, 0, 51, 0, 0, 0, 0, 0])   # :
    
    assert len(lst) == 8, 'Invalid data length (needs 8 bytes)'
    conv_table = {
        0:['', ''],
        4:['a', 'A'],
        5:['b', 'B'],
        6:['c', 'C'],
        7:['d', 'D'],
        8:['e', 'E'],
        9:['f', 'F'],
        10:['g', 'G'],
        11:['h', 'H'],
        12:['i', 'I'],
        13:['j', 'J'],
        14:['k', 'K'],
        15:['l', 'L'],
        16:['m', 'M'],
        17:['n', 'N'],
        18:['o', 'O'],
        19:['p', 'P'],
        20:['q', 'Q'],
        21:['r', 'R'],
        22:['s', 'S'],
        23:['t', 'T'],
        24:['u', 'U'],
        25:['v', 'V'],
        26:['w', 'W'],
        27:['x', 'X'],
        28:['y', 'Y'],
        29:['z', 'Z'],
        30:['1', '!'],
        31:['2', '@'],
        32:['3', '#'],
        33:['4', '$'],
        34:['5', '%'],
        35:['6', '^'],
        36:['7' ,'&'],
        37:['8', '*'],
        38:['9', '('],
        39:['0', ')'],
        40:['\n', '\n'],
        41:['\x1b', '\x1b'],
        42:['\b', '\b'],
        43:['\t', '\t'],
        44:[' ', ' '],
        45:['_', '_'],
        46:['=', '+'],
        47:['[', '{'],
        48:[']', '}'],
        49:['\\', '|'],
        50:['#', '~'],
        52:["'", '"'],
        53:['`', '~'],
        54:[',', '<'],
        55:['.', '>'],
        56:['/', '?'],
        100:['\\', '|'],
        103:['=', '='],
        }

    # A 2 in first byte seems to indicate to shift the key. For example
    # a code for ';' but with 2 in first byte really means ':'.
    if lst[0] == 2:
        shift = 1
    else:
        shift = 0
        
    # The character to convert is in the third byte
    ch = lst[2]
    if ch not in conv_table:
        print("Warning: data not in conversion table")
        logger.log("[Warning!] USB HID char code not in conversion table")
        return ''
    return conv_table[ch][shift]

def apiCall(UPCcode):
    # plug scanned UPC code into url for api call
    url = 'https://world.openfoodfacts.net/api/v2/product/' + UPCcode + '?product_type=all&cc=us&lc=en&fields=product_name&blame=0'
    useragent = 'InventorySystem/0.1 (' + email + ')'
    headers = {'accept': 'application/json', 'User-Agent': useragent}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Parse JSON data automatically
        data = response.json()
        # log all successful api calls to aid with troubleshooting failiures due to rate limiting
        logger.log("api call successful, code: " + data["code"] + " returned: " + data["product"]["product_name"])
        return(data)
    else:
        # log http errors
        logger.log(f"[Warning!] api call failed with status code: {response.status_code}")

def pollInput():
    line = ''
    char1 = 'X'
    char2 = 'X'
    char3 = 'X'
    char4 = 'X'
    while True:
        char1 = readLine(L1, [";1",";2",";3",";A"])
        char2 = readLine(L2, [";4",";5",";6",";B"])
        char3 = readLine(L3, [";7",";8",";9",";C"])
        char4 = readLine(L4, [";*",";0",";#",";D"])
        if (char1 != 'X'):
            return(char1)
        elif(char2 != 'X'):
            return(char2)
        elif(char3 != 'X'):
            return(char3)
        elif(char4 != 'X'):
            return(char4)
        else:
            pass
        try:
            # Wait up to 0.5 seconds for data. 500 = 0.5 second timeout.
            data = ep.read(1000, 500)  
            ch = hid2ascii(data)
            line += ch
            if  ch == '\n' and len(line) > 0:
                return line
        except KeyboardInterrupt:    # if a scan somehow throws a keyboard interrupt, catch it
            print("Stopping program")
            logger.log("Keyboard interrupt intercepted, exiting program")
            dev.reset()
            if needs_reattach:
                dev.attach_kernel_driver(0)
                logger.log("Reattached USB device to kernel driver")
                print("Reattached USB device to kernel driver")
            return
        except core.USBTimeoutError:
            continue

def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        return(characters[0])
    elif(GPIO.input(C2) == 1):
        return(characters[1])
    elif(GPIO.input(C3) == 1):
        return(characters[2])
    elif(GPIO.input(C4) == 1):
        return(characters[3])
    else:
        return('X')
    GPIO.output(line, GPIO.LOW)


# Find our device using the VID (Vendor ID) and PID (Product ID)
dev = core.find(idVendor=0x05e0, idProduct=0x1200)                  # IF YOU USE A DIFFERENT SCANER, CHANGE THESE VALUES
if dev is None:
    raise ValueError('USB device not found')

# Disconnect it from kernel
needs_reattach = False
if dev.is_kernel_driver_active(0):
    needs_reattach = True
    dev.detach_kernel_driver(0)
    logger.log("Detached USB device from kernel driver")
    print("Detached USB device from kernel driver")

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = util.find_descriptor(
    intf,
    # match the first IN endpoint
    custom_match = \
    lambda e: \
        util.endpoint_direction(e.bEndpointAddress) == \
        util.ENDPOINT_IN)

assert ep is not None, "Endpoint for USB device not found. Something is wrong."

# Loop through a series of 8-byte transactions and convert each to an
# ASCII character. Print output after 0.5 seconds of no data.

# Initialize the GPIO pins




print(pollInput())

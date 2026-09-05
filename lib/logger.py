import time


def log(entry):
    try:
        with open("inventorySystem.log", "x", encoding="utf-8") as log:
            log.write("[")
            log.write(time.ctime())
            log.write("] new log file created\n")
    except FileExistsError:
        pass

    if(len(entry) > 0):
        with open("inventorySystem.log", "a", encoding="utf-8") as log:
            log.write("[")
            log.write(time.ctime())
            log.write("] " + entry + "\n")
    
    else:
        with open("inventorySystem.log", "a", encoding="utf-8") as log:
            log.write("[")
            log.write(time.ctime())
            log.write("] log file write of length 0 attempted, throwing exception\n")
            raise ValueError("log file write of length 0 attempted")



    
    



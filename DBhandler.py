import sqlite3


db = sqlite3.connect('/home/pi/the inventory project/inventorySystem.db')
cursor = db.cursor()


def newData(code, name, size, brand, quantity):
    db.connect()
    Inventory.insert(code=code, product_name=name, product_size=size, brand=brand, quantity=quantity).execute()
    db.close()

def queryData(code):
    try:
        cursor.execute("SELECT * FROM inventory WHERE code = " + code + ";")
    except:
        return None
    else:
        data = cursor.fetchone()
        return (data)



def editData(code, diff):
    db.connect()
    data = Inventory.get_or_none(Inventory.code == code)
    data.quantity += diff
    data.save()
    db.close()




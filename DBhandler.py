"""
    Copyright (C) 2026 Alan Fine

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

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




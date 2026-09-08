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
import sys
sys.path.append('./lib')
import logger

db = sqlite3.connect('inventorySystem.db')
cursor = db.cursor()


def newData(code, name, size, brand, quantity):
    logger.log('[DB] creating new DB entry for ' + code)
    code2 = code.lstrip('0')
    cursor.execute('insert into inventory (code, product_name, product_size, brand, quantity) values (' + code + ', ' + name + ', ' + size + ', ' + brand + ', ' + quantity + ');')

def queryData(code):
    logger.log('[DB] attempting DB query of code: ' + code)
    code2 = code.lstrip('0')
    try:
        cursor.execute("SELECT * FROM inventory WHERE code = " + code2 + ";")
        logger.log(code2)
    except:
        logger.log('[DB] Code ' + code + ' not found in DB')
        return None
    else:
        data = cursor.fetchone()
        logger.log('[DB] found match for code' + code + 'in DB')
        return (data)



def editData(code, diff):
    db.connect()
    data = Inventory.get_or_none(Inventory.code == code)
    data.quantity += diff
    data.save()
    db.close()




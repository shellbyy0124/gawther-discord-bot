import sqlite3 as sql

from datetime import datetime

with sql.connect('main.db') as mdb:
    cur = mdb.cursor()

    user_id = 785294763258806302

    srch = 'SELECT * FROM kick_logs WHERE id=?'
    val = (user_id,)

    all_logs = cur.execute(srch, val).fetchall()
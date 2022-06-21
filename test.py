import sqlite3 as sql

choice = "Mute"
titles = ["ID","Exp","Level","Warnings","Mutes","Kicks","Bans"]
titles2 = ["ID","Log ID","Staff Member","Start Time","End Time","Reason"]

with sql.connect('main.db') as mdb:
    cur = mdb.cursor()

    srch = 'SELECT id,exp,level,warnings,mutes,bans,kicks FROM members WHERE Id=?'
    val = (785294763258806302,)

    srch2 = f'SELECT * FROM {choice.lower()}_logs WHERE id=?'
    val2 = (785294763258806302,)

    all_mem_info = cur.execute(srch, val).fetchall()
    all_log_info = cur.execute(srch2, val2).fetchall()

    for title in titles:
        value=f"{title}: {all_mem_info[0][titles.index(title)]}"
        print(value)

    for title2 in titles2:
        value=f"{title2}: {all_log_info[0][titles2.index(title2)]}"
        print(value)
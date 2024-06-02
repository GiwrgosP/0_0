import sqlite3


def conn(path):
    str = path +"\\db.db"
    try:
        con = sqlite3.connect(str)
        c = con.cursor()
        return con,c
    except:
        print("Error While Connectiong To DataBase", str)


def get(path,sqlC):
    con,c = conn(path)
    str, value = sqlC
    c.execute(str,value)
    rows = c.fetchall()
    con.close()
    return rows

def add(path,sqlC):
    print(sqlC)
    con,c = conn(path)
    str, value = sqlC
    c.execute(str,value)
    con.commit()
    con.close()

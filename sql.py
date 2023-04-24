import sqlite3 as sql
def sql_qu(query):
    dbname='record.db'
    con=sql.connect(dbname)
    cursor=con.cursor()
    cursor.execute(query)
    result=cursor.fetchall()
    con.commit()
    cursor.close()
    con.close()
    return result
result=sql_qu("CREATE TABLE students_marks(email VARCHAR(200) PRIMARY KEY, hindi INTEGER, english INTEGER, maths INTEGER, chemistry INTEGER, physics INTEGER, CONSTRAINT `FK` FOREIGN KEY (email) REFERENCES user(email))")
print(result)


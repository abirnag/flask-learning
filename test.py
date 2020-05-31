import sqlite3 

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table ="CREATE TABLE USERS (id int, username text, password text)"

cursor.execute(create_table)

users = [(1,"abir","1234"),(2,"abir1","1234"),(3,"abir2","1234")]

insert_query = "INSERT INTO USERS VALUES(?,?,?)"

cursor.executemany(insert_query,users)

select_query = "SELECT * FROM USERS"
for row in cursor.execute(select_query):
    print(row)
connection.commit()
connection.close()


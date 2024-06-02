import sqlite3

connection = sqlite3.connect("testMSGs.db")
c = connection.cursor()

def createDB(tableName):
    query = f"CREATE TABLE IF NOT EXISTS {tableName}(msg TEXT)"
    c.execute(query)

def showDB():
    c.execute("SELECT * FROM msgTable")
    database = c.fetchall()
    for row in database:
        print(row)

def addToTableDB(table, value):
    query = f"INSERT INTO {table} VALUES ('{value}')"
    c.execute(query)
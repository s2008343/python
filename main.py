#!/usr/bin/python
import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='presentatie',
                                         user='Cas',
                                         password='hNZtYCDk7xk81XUPKPT6')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        sql_select_Query = "select id, login from members"
        cursur = connection.cursor()
        cursur.execute(sql_select_Query)
        records = cursor.fetchall()
        print("Total number of rows in table",cursor.rowcount)




        for row in records:
            print(row[0], row[1])


        cursor.close()
        connection.close()
        print("MySQL connection is closed")







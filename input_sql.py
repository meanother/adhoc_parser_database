#!/usr/bin/python3
import psycopg2


def connect_to_database(querry):
    connect = psycopg2.connect(dbname='parsing_db',
                               user='semenov',
                               password='12345',
                               host='localhost',
                               port=5432)
    connect.autocommit = True
    cursor = connect.cursor()
    cursor.execute(querry)
    for row in cursor:
        print(row)
    cursor.close()
    connect.close()


querry = input('pls enter the sql-querry: ')
connect_to_database(str(querry))





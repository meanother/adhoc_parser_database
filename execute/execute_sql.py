#!/usr/bin/python3
import psycopg2


def connect_to_database(file):
    connect = psycopg2.connect(dbname='manjaro_db',
                               user='semenov',
                               password='',
                               host='localhost',
                               port=5432)
    connect.autocommit = True
    cursor = connect.cursor()
    with open(file, 'r') as file:
        cursor.execute(file.read())
        try:
            for row in cursor:
                print(row)
        except psycopg2.ProgrammingError:
            pass
    cursor.close()
    connect.close()


file = 'create.sql'
connect_to_database(file)





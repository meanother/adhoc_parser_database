#!/usr/bin/python3
import psycopg2


def connect_to_database(file):
    connect = psycopg2.connect(dbname='parsing_db',
                               user='semenov',
                               password='12345',
                               host='localhost',
                               port=5432)
    connect.autocommit = True
    cursor = connect.cursor()
    with open(file, 'r') as file:
        rlist = file.read()
        list = rlist.replace('\n', '').split(';')
        for script in list[:-1]:
            cursor.execute(script)
            try:
                for row in cursor:
                    print(row)
            except psycopg2.ProgrammingError:
                pass
    cursor.close()
    connect.close()


file = 'create_table.sql'
connect_to_database(file)





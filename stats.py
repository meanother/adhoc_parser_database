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


querry = '''
select * from (
select name 'kludi_com',count(*), parse_date from adhoc_parser.kludi_com group by datex
union
select name'grohe', count(*), parse_date from adhoc_parser.grohe group by datex
union
select name'pergo', count(*), parse_date from adhoc_parser.pergo group by datex
union
select name'pratta', count(*), parse_date from adhoc_parser.pratta group by datex
union
select name'quick-step', count(*), parse_date from adhoc_parser.quick_step group by datex
union
select name'sunerzha', count(*), parse_date from adhoc_parser.sunerzha group by datex) as foo
order by name;
'''
connect_to_database(str(querry))





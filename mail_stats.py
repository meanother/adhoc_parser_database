#!/usr/bin/python3

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
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
select name 'kludi_com',count(*), parse_date from adhoc_parser.kludi_com group by parse_date
union
select name'grohe', count(*), parse_date from adhoc_parser.grohe group by parse_date
union
select name'pergo', count(*), parse_date from adhoc_parser.pergo group by parse_date
union
select name'pratta', count(*), parse_date from adhoc_parser.pratta group by parse_date
union
select name'quick-step', count(*), parse_date from adhoc_parser.quick_step group by parse_date
union
select name'sunerzha', count(*), parse_date from adhoc_parser.sunerzha group by parse_date) as foo
order by name;
'''

order = connect_to_database(str(querry))


msg = MIMEMultipart()
msg['Subject'] = 'Number of rows in tables'
msg['From'] = 'juicehqperfect@gmail.com'
msg['To'] = 'juicehq@yandex.ru'


message = 'look at me: \n' + str(order)

part = MIMEText(message, 'plain')
msg.attach(part)

passw = str(input('pls enter the password: '))
server = smtplib.SMTP('smtp.gmail.com:587')
server.set_debuglevel(True)
server.starttls()
server.login('juicehqperfect@gmail.com', passw)
server.send_message(msg)
server.quit()



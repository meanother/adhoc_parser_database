#!/usr/bin/python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
import datetime

def get_componentns():
    parse_date = str(datetime.date.today())
    command = f'''
    psql -U semenov -d parsing_db -h localhost -w -c "select * from (
    select name 'oracdecor_KAFKA',count(*), parse_date from adhoc_parser.oracdecor where parse_date = '{parse_date}' group by parse_date
    union
    select name 'kludi_com',count(*), parse_date from adhoc_parser.kludi_com where parse_date = '{parse_date}' group by parse_date
    union
    select name 'grohe', count(*), parse_date from adhoc_parser.grohe where parse_date = '{parse_date}' group by parse_date
    union
    select name 'pergo', count(*), parse_date from adhoc_parser.pergo where parse_date = '{parse_date}' group by parse_date
    union
    select name 'pratta', count(*), parse_date from adhoc_parser.pratta where parse_date = '{parse_date}' group by parse_date
    union
    select name 'quick-step', count(*), parse_date from adhoc_parser.quick_step where parse_date = '{parse_date}' group by parse_date
    union
    select name 'sunerzha', count(*), parse_date from adhoc_parser.sunerzha where parse_date = '{parse_date}' group by parse_date
    union
    select name 'stilye', count(*), parse_date from adhoc_parser.stilye where parse_date = '{parse_date}' group by parse_date
    union
    select name 'qq_stilye', count(*), parse_date from adhoc_parser.qq_stilye where parse_date = '{parse_date}' group by parse_date
    union
    select name 'perfect_msk', count(*), parse_date from adhoc_parser.perfect_msk where parse_date = '{parse_date}' group by parse_date
    ) as foo
    order by name;"
    '''
    my_env = {'PGPASSWORD':'12345'}
    comps = []
    command = subprocess.Popen(command, shell=True, env=my_env, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    components = command.communicate()
    #print(components)
    for i in components:
        try:
            component = i.decode('utf-8')
            comps.append(component)
            #print(component)
        except AttributeError:
            pass
    return comps



message = '\n'.join(get_componentns())

html_intro = '<html><head><meta charset="cp1251"></head><body>'
html_output = ('<tt><br />{}<br /></tt>'.format(message))
html_outro = '</body></html>'
#send_message(RCPLIST, html_intro+html_output+html_outro)



msg = MIMEMultipart()
msg['Subject'] = 'Number of rows in tables'
msg['From'] = 'juicehqperfect@gmail.com'
msg['To'] = 'juicehq@yandex.ru'


#message = (" ".join(str(x) for x in order)).replace(' ', '\n')
#message = ("//".join(str(x) for x in order).replace('//', '\n'))



part = MIMEText(message, 'plain')
msg.attach(part)

passw = input('password')
server = smtplib.SMTP('smtp.gmail.com:587')
server.set_debuglevel(True)
server.starttls()
server.login('juicehqperfect@gmail.com', passw)
server.send_message(msg)
#server.send_message(html_intro + html_output + html_outro)
server.quit()

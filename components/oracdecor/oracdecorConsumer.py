#!/usr/bin/python3
from kafka import KafkaProducer, KafkaConsumer
import json
import psycopg2


def connect_to_database(name, category, specification, avaliable_text, overview, scheme_picture, banner, main_pic, price_metr, price_one, big_pic, text, pdf, link, today_time):
    with open('/home/ubpc/adhoc_parser_database/components/oracdecor/config.json', 'r') as file1:
    #with open('/home/arty/python/adhoc_parser/components/stilye/config.json', 'r') as file1:
        data = json.loads(file1.read())
        connect = psycopg2.connect(dbname=data['dbname'],
        #connect = psycopg2.connect(dbname='manjaro_db',
                                   user=data['user'],
                                   #user='semenov',
                                   #password='',
                                   password=data['password'],
                                   host=data['host'],
                                   #host='localhost',
                                   port=data['port'])
                                   #port=5432)
        connect.autocommit = True
        cursor = connect.cursor()
        cursor.execute('''
        INSERT INTO adhoc_parser.oracdecor
        (name, category, specifications, avaliable_text, overview, scheme_picture, banner, picture, price_metr, price_one, big_pic, text, pdf, link, parse_date) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (name, category, specification, avaliable_text, overview, scheme_picture, banner, main_pic, price_metr, price_one, big_pic, text, pdf, link, today_time))
        cursor.close()
        connect.close()



consumer = KafkaConsumer(
    'oracdecor',
    group_id='one_gr',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')))

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    #print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
    #                                      message.offset, message.key,
    #                                      message.value))

    datax = message.value
    connect_to_database(
        datax['name'],
        datax['category'],
        datax['specifications'],
        datax['available_text'],
        datax['overview'],
        datax['scheme_picture'],
        datax['banner'],
        datax['max_tag'],
        datax['price_metr'],
        datax['price_one'],
        datax['big_pic'],
        datax['text'],
        datax['pdfs'],
        datax['link'],
        datax['parse_date']
    )
    print('Message inserted successfull ' + str(message.value))

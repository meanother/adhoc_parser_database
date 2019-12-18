#!/usr/bin/python3
from kafka import KafkaProducer, KafkaConsumer
import json
import psycopg2


def connect_to_database_home(name, articul, category1, category2, feature, description, produce, price, picture, recomended, complect , today_time):
    with open('/home/arty/python/adhoc_parser/components/perfect_msk/config.json', 'r') as file1:
        data = json.loads(file1.read())
        connect = psycopg2.connect(dbname='manjaro_db',
                                   user='semenov',
                                   password='',
                                   host='localhost',
                                   port=5432)
        connect.autocommit = True
        cursor = connect.cursor()
        cursor.execute('''
        INSERT INTO cr_model.perfect_msk
        (name, articul, category1, category2, feature, description, produce, price, picture, recomended, complect, parse_date) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (name, articul, category1, category2, feature, description, produce, price, picture, recomended, complect, today_time))
        cursor.close()
        connect.close()






def connect_to_database_prod(name, articul, category1, category2, feature, description, produce, price, picture, recomended, complect , today_time):
    with open('/home/ubpc/adhoc_parser_database/components/perfect_msk/config.json', 'r') as file1:
        data = json.loads(file1.read())
        connect = psycopg2.connect(dbname=data['dbname'],
                                   user=data['user'],
                                   password=data['password'],
                                   host=data['host'],
                                   port=data['port'])
        connect.autocommit = True
        cursor = connect.cursor()
        cursor.execute('''
        INSERT INTO adhoc_parser.perfect_msk
        (name, articul, category1, category2, feature, description, produce, price, picture, recomended, complect, parse_date) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (name, articul, category1, category2, feature, description, produce, price, picture, recomended, complect, today_time))
        cursor.close()
        connect.close()


consumer = KafkaConsumer(
    'perfect_msk',
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
    connect_to_database_prod(
        datax['name'],
        datax['articul'],
        datax['category1'],
        datax['category2'],
        datax['feature'],
        datax['description'],
        datax['produce'],
        datax['price'],
        datax['picture'],
        datax['recomended'],
        datax['complect'],
        datax['parse_date']
    )
    print('Message inserted successfull ' + str(message.value))







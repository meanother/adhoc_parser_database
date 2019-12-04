from kafka import KafkaProducer, KafkaConsumer
import json


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
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))
    print(message.headers)
    metrics = consumer.metrics()
    print(metrics)
    '''
    print(message.topic)
    print(message.partition)
    print(message.offset)
    print(message.key)
    print(message.value)
    data = message.value
    print(type(message.value))

    print(data['name'])
    print(data['category'])
    print(data['specifications'])
    print(data['available_text'])
    print(data['overview'])
    print(data['scheme_picture'])
    print(data['banner'])
    print(data['max_tag'])
    print(data['price_metr'])
    print(data['price_one'])
    print(data['big_pic'])
    print(data['text'])
    print(data['pdfs'])
    print(data['link'])
    '''


    print('---------------------')
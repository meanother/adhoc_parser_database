import json


#with open('config.json', 'w') as file:
#    dict = {'name': 'Artur', 'second_name': 'Semenov'}
#    json.dump(dict, file)


with open('config.json', 'r') as file1:
    data = json.loads(file1.read())
    print(data)

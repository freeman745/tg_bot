import pymongo


db_client = pymongo.MongoClient(host='localhost', port=27017)

db = db_client['test']

bot_hub = db['test']

#s = {'token': '111','name':'fdgh'}
#result = bot_hub.insert_one(s)
#print(result)

#result = bot_hub.find_one({'token': '333'})
result = bot_hub.find()
'''
if result:
    print(result['name'])
else:
    print('!!!')
'''
#print(bot_hub.delete_many({'token':'333'}))
print(result)
for i in result:
    print(i)

import requests
import sys
import json


headers = {'Content-type':'application/json'}
# 读取命令行参数
if len(sys.argv) > 1:
    test = sys.argv[1]
    if test == 'create':
        new_bot = {'bot_name' : 'test',
                   'bot_user_name' : 'test',
                   'token' : '6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c',
                   'create_time' : 'test',
                   'owner' : 'test',
                   'bot_address' : 'test'}
        url = 'http://127.0.0.1:4000/create_bot'
        response = requests.post(url, json=new_bot)
    if test == 'delete':
        data = {
            'token': '6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c'
        }
        url = 'http://127.0.0.1:4000/delete_bot'
        response = requests.post(url, json=data)
    if test == 'edit':
        data = {
            'old_token': '6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c',
            'bot_name': 't',
            'bot_user_name':'t',
            'token':'6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c',
            'bot_address':'t'
        }
        url = 'http://127.0.0.1:4000/edit_bot'
        response = requests.post(url, json=data)
    if test == 'ban':
        data = {'token':'6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c', 'chat_id':'-1002132190433','user_id':'5466032236','ban_time':'120'}
        url = 'http://127.0.0.1:4000/ban'
        response = requests.post(url, json=data)
    if test == 'unban':
        data = {'token':'6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c', 'chat_id':'-1002132190433','user_id':'5466032236'}
        url = 'http://127.0.0.1:4000/unban'
        response = requests.post(url, json=data)
    if test == 'kick':
        data = {'token':'6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c', 'chat_id':'-1002132190433','user_id':'5466032236'}
        url = 'http://127.0.0.1:4000/kick'
        response = requests.post(url, json=data)
    if test == 'list':
        url = 'http://127.0.0.1:4000/list_bot'
        response = requests.post(url)
    if test == 'group_info':
        data = {'token': '6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c'}
        url = 'http://127.0.0.1:4000/group_info'
        response = requests.post(url, json=data, headers=headers)
    if test == 'set_group_name':
        data = {'token':'6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c', 'chat_id':'-1002132190433','new_group_name':'heiheihei'}
        url = 'http://127.0.0.1:4000/set_group_name'
        response = requests.post(url, json=data, headers=headers)
    if test == 'set_group_des':
        data = {'token':'6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c', 'chat_id':'-1002132190433','new_group_description':'heihei'}
        url = 'http://127.0.0.1:4000/set_group_description'
        response = requests.post(url, json=data, headers=headers)
else:
    print("No variable provided.")

print(print(json.dumps(json.loads(response.text),  ensure_ascii=False)))


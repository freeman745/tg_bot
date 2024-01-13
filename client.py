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
                   'token' : '6827752624:AAGOc-IO8QlQE3vxfB-4j5W2a2MTAHcT67E',
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
    if test == 'list_bot':
        url = 'http://127.0.0.1:4000/list_bot'
        response = requests.post(url)
    if test == 'group_info':
        #data = {'token': '6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c'}
        data = {'token': '6827752624:AAGOc-IO8QlQE3vxfB-4j5W2a2MTAHcT67E'}
        url = 'http://127.0.0.1:4000/group_info'
        response = requests.post(url, json=data, headers=headers)
    if test == 'set_group_name':
        data = {'token':'6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c', 'chat_id':'-1002132190433','new_group_name':'heiheihei','new_group_description':'heihei'}
        url = 'http://127.0.0.1:4000/set_group_name_description'
        response = requests.post(url, json=data, headers=headers)
    if test == 'set_group_des':
        data = {'token':'6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c', 'chat_id':'-1002132190433','new_group_description':'heihei'}
        url = 'http://127.0.0.1:4000/set_group_description'
        response = requests.post(url, json=data, headers=headers)
    if test == 'add_template':
        data = {'template_name':'test',
                'description':'test',
                'template':'test',
                'create_time':'test',
                'owner':'test',
                'status':'heihei'}
        url = 'http://127.0.0.1:4000/add_template'
        response = requests.post(url, json=data, headers=headers)
    if test == 'show_template':
        data = {'template_name':'test'}
        url = 'http://127.0.0.1:4000/show_template'
        response = requests.post(url, json=data, headers=headers)
    if test == 'edit_template':
        data = {'old_template_name':'test',
                'template_name' : 'new_name',
                'description' : 'description',
                'template' : 'template',
                'status' : 'Disable'}
        url = 'http://127.0.0.1:4000/edit_template'
        response = requests.post(url, json=data, headers=headers)
    if test == 'delete_template':
        data = {'template_name':'new_name'}
        url = 'http://127.0.0.1:4000/delete_template'
        response = requests.post(url, json=data, headers=headers)
    if test == 'list_template':
        url = 'http://127.0.0.1:4000/list_template'
        response = requests.post(url)
    if test == 'preview_message':
        data = {'message_content':'hello','button':[{'button_name':'test1', 'url':'www.baidu.com'}, {'button_name':'test2', 'url':'www.google.com'}]}
        url = 'http://127.0.0.1:4000/preview_message'
        response = requests.post(url, json=data, headers=headers)
    if test == 'send_message':
        data = {'message_name':'test',
                'message_content':'hello',
                'button':[{'button_name':'test1', 'url':'www.baidu.com'}, {'button_name':'test2', 'url':'www.google.com'}],
                'template':'t',
                'owner':'t',
                'schedule':10,
                'create_time':0,
                'delete_time':3,
                'send_time':0,
                'send_groups':['heiheihei']}
        url = 'http://127.0.0.1:4000/send_message'
        response = requests.post(url, json=data, headers=headers)
    if test == 'kill_message':
        data = {'message_name':'test'}
        url = 'http://127.0.0.1:4000/kill_message'
        response = requests.post(url, json=data, headers=headers)
    if test == 'login':
        data = {'user_name':'admin', 'password':'admin', 'captcha':'eOnA'}
        url = 'http://127.0.0.1:4000/login'
        response = requests.post(url, json=data, headers=headers)
    if test == 'register':
        data = {'user_name':'admin', 'password':'admin', 'isAdmin':'True'}
        url = 'http://127.0.0.1:4000/register'
        response = requests.post(url, json=data, headers=headers)
    if test == 'captcha':
        url = 'http://127.0.0.1:4000/captcha'
        response = requests.get(url)
        with open('t.png', 'wb') as f:
            f.write(response.content)
    if test == 'list_user':
        url = 'http://127.0.0.1:4000/list_user'
        response = requests.get(url)
    if test == 'list_group':
        url = 'http://127.0.0.1:4000/list_group'
        response = requests.post(url)
else:
    print("No variable provided.")

print(json.dumps(json.loads(response.text),  ensure_ascii=False))


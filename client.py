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
        url = 'http://127.0.0.1:5000/create_bot'
        response = requests.post(url, json=new_bot)
    if test == 'delete':
        data = {
            'token': ''
        }
        url = 'http://127.0.0.1:5000/delete_bot'
        response = requests.post(url, json=data)
    if test == 'edit':
        data = {
            'old_token': '6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c',
            'bot_name': 't',
            'bot_user_name':'t',
            'token':'6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c',
            'bot_address':'t'
        }
        url = 'http://127.0.0.1:5000/edit_bot'
        response = requests.post(url, json=data)
    if test == 'ban':
        data = {'token':'6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c', 'chat_id':'-1002132190433','user_id':'5466032236','ban_time':'120'}
        url = 'http://127.0.0.1:5000/ban'
        response = requests.post(url, json=data)
    if test == 'unban':
        data = {'token':'6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c', 'chat_id':'-1002132190433','user_id':'5466032236'}
        url = 'http://127.0.0.1:5000/unban'
        response = requests.post(url, json=data)
    if test == 'kick':
        data = {'token':'6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c', 'chat_id':'-1002132190433','user_id':'5466032236'}
        url = 'http://127.0.0.1:5000/kick'
        response = requests.post(url, json=data)
    if test == 'list_bot':
        data = {'page_index':'3','per_page':'1'}
        url = 'http://127.0.0.1:5000/list_bot'
        response = requests.post(url, json=data)
    if test == 'group_info':
        data = {'token': '6827752624:AAGOc-IO8QlQE3vxfB-4j5W2a2MTAHcT67E'}
        url = 'http://127.0.0.1:5000/group_info'
        response = requests.post(url, json=data, headers=headers)
    if test == 'set_group_name':
        data = {'token':'6827752624:AAGOc-IO8QlQE3vxfB-4j5W2a2MTAHcT67E', 'chat_id':'-1002045238641,','new_group_name':'Freman_ZFDC and Carson_ZFDC1','new_group_description':'Test Group'}
        url = 'http://127.0.0.1:5000/set_group_name_description'
        response = requests.post(url, json=data, headers=headers)
    if test == 'set_group_des':
        data = {'token':'6928667476:AAH26L8dcywZnNTWVyOrBH499z56OpNbd5c', 'chat_id':'-1002132190433','new_group_description':'heihei'}
        url = 'http://127.0.0.1:5000/set_group_description'
        response = requests.post(url, json=data, headers=headers)
    if test == 'add_template':
        data = {'template_name':'test',
                'description':'test',
                'template':'test',
                'create_time':'test',
                'owner':'test',
                'status':'heihei'}
        url = 'http://127.0.0.1:5000/add_template'
        response = requests.post(url, json=data, headers=headers)
    if test == 'show_template':
        data = {'template_name':'test'}
        url = 'http://127.0.0.1:5000/show_template'
        response = requests.post(url, json=data, headers=headers)
    if test == 'edit_template':
        data = {'old_template_name':'test',
                'template_name' : 'new_name',
                'description' : 'description',
                'template' : 'template',
                'status' : 'Disable'}
        url = 'http://127.0.0.1:5000/edit_template'
        response = requests.post(url, json=data, headers=headers)
    if test == 'delete_template':
        data = {'template_id':'54571311852'}
        url = 'http://127.0.0.1:5000/delete_template'
        response = requests.post(url, json=data, headers=headers)
    if test == 'list_template':
        url = 'http://127.0.0.1:5000/list_template'
        response = requests.post(url)
    if test == 'preview_message':
        data = {'chat_id':'-1002045238641','message_content':'hello','button':[{'button_name':'test1', 'url':'www.baidu.com'}, {'button_name':'test2', 'url':'www.google.com'}]}
        url = 'http://127.0.0.1:5000/preview_message'
        response = requests.post(url, json=data, headers=headers)
    if test == 'send_message':
        data = {'message_name':'333',
                'message_content':'<p>啦啦啦33</p>',
                'button':[{'button_name':'test1', 'url':'www.baidu.com'}, {'button_name':'test2', 'url':'www.google.com'}],
                'template':'312848844455',
                'owner':'admin',
                'schedule':-1,
                'create_time':"2024-01-17 20:24:10",
                'delete_time':-1,
                'send_time':0,
                'send_groups':['Sage_ZFDC & Sage','Freman_ZFDC and Carson_ZFDC12']}
        url = 'http://127.0.0.1:5000/send_message'
        response = requests.post(url, json=data, headers=headers)
    if test == 'kill_message':
        data = {'message_name':'test'}
        url = 'http://127.0.0.1:5000/kill_message'
        response = requests.post(url, json=data, headers=headers)
    if test == 'login':
        data = {'user_name':'aaaa','password':'abbbb','captcha':'aaa'}
        url = 'http://127.0.0.1:5000/login'
        response = requests.post(url, json=data, headers=headers)
    if test == 'register':
        data = {'user_name':'admin','password':'admin','isAdmin':'True'}
        url = 'http://127.0.0.1:5000/register'
        response = requests.post(url, json=data, headers=headers)
    if test == 'list_user':
        data = {'page_index':'1','per_page':'1','user_name':'carson'}
        url = 'http://127.0.0.1:5000/list_user'
        response = requests.post(url, json=data)
    if test == 'list_group':
        #data = {'page_index':'1','per_page':'1'}
        data = {}
        url = 'http://127.0.0.1:5000/list_group'
        response = requests.post(url, json=data)
    if test == 'search_message':
        data = {'page_index':'1', 'per_page':'1'}
        url = 'http://127.0.0.1:5000/search_message'
        response = requests.post(url, json=data, headers=headers)
    if test == 'delete_message':
        data = {'message_id':'901568449877'}
        url = 'http://127.0.0.1:5000/delete_message'
        response = requests.post(url, json=data, headers=headers)
    if test == 'edit_user':
        data = {'id':'679473538777','user_name':'admin','password':'123456','status':'启用'}
        url = 'http://127.0.0.1:5000/edit_user'
        response = requests.post(url, json=data, headers=headers)
else:
    print("No variable provided.")

print(json.dumps(json.loads(response.text),  ensure_ascii=False))
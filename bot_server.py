from flask import Flask, request, jsonify
from telegram import Bot, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup
import time
import json
import pymongo
import random
import multiprocessing
import io
from captcha.image import ImageCaptcha
import string


app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

db_client = pymongo.MongoClient(host='localhost', port=27017)

db = db_client['telegram']

worker_hub = {}

captcha_save = ''

preview_code_list = []

def auto_delete(chat_id, message_id, token, delete_time):
    bot = Bot(token)
    time.sleep(delete_time)
    bot.delete_message(chat_id=chat_id, message_id=message_id)


def send_message_worker(message_id, chat_bot_match, message_content, button, send_time, schedule, delete_time):
    global db
    message_hub = db['message_hub']
    if button:
        keyboard = []
        for i in button:
            keyboard.append([InlineKeyboardButton(i['button_name'], url=i['url'])])
        keyboard = InlineKeyboardMarkup(keyboard)

    if schedule > 0:
        while True:
            if time.time() < send_time:
                continue
            for chat_id in chat_bot_match:
                token = chat_bot_match[chat_id]
                bot = Bot(token)
                if button:
                    sent_message = bot.send_message(chat_id=chat_id, text=message_content, reply_markup=keyboard)
                else:
                    sent_message = bot.send_message(chat_id=chat_id, text=message_content)
                if delete_time > 0:
                    worker_process = multiprocessing.Process(target=auto_delete,args=(chat_id, sent_message.message_id, token, delete_time))

                    worker_process.start()
            condition = {"message_id": message_id}
            update_data = {"$set": {"status": "待发送", "end_time":int(time.time())}}
            message_hub.update_one(condition, update_data)
            time.sleep(schedule)
    else:
        while True:
            if time.time() < send_time:
                continue
            for chat_id in chat_bot_match:
                token = chat_bot_match[chat_id]
                bot = Bot(token)
                if button:
                    sent_message = bot.send_message(chat_id=chat_id, text=message_content, reply_markup=keyboard)
                else:
                    sent_message = bot.send_message(chat_id=chat_id, text=message_content)
                if delete_time > 0:
                    worker_process = multiprocessing.Process(target=auto_delete,args=(chat_id, sent_message.message_id, token, delete_time))

                    worker_process.start()
            condition = {"message_id": message_id}
            update_data = {"$set": {"status": "已发送", "end_time":int(time.time())}}
            message_hub.update_one(condition, update_data)
            break


def preview_message_worker(bot_token, preview_code, message_content, button):
    global preview_code_list
    start = int(time.time())
    bot = Bot(bot_token)
    chat_id = ''
    while (int(time.time()) - start) <= 15*60:
        updates = bot.get_updates()
        for update in updates:
            if str(update.message['text']) == preview_code:
                chat_id = update.message.chat_id
                break
        time.sleep(5)

    if not chat_id:
        return 0
    
    if button:
        keyboard = []
        for i in button:
            keyboard.append([InlineKeyboardButton(i['button_name'], url=i['url'])])
        keyboard = InlineKeyboardMarkup(keyboard)
        sent_message = bot.send_message(chat_id=chat_id, text=message_content, reply_markup=keyboard)
    else:
        sent_message = bot.send_message(chat_id=chat_id, text=message_content)

    preview_code_list.remove(preview_code)
    

# health check
@app.route('/health', methods=['GET'])
def health_check():
    response = {'code': 200, 'error': 'success'}
    return jsonify(response)


@app.route('/create_bot', methods=['POST'])
def create_bot():
    try:
        global db
        data = request.json
        bot_hub = db['bot_hub']
        token = data['token']
        search = bot_hub.find_one({'token': token})
        if search:
            response = {'code': 310, 'error': 'Bot already created!'}
            return jsonify(response)
        try:
            bot_name = data['bot_name']
        except:
            bot_name = ''
        bot_user_name = data['bot_user_name']
        create_time = data['create_time']
        owner = data['owner']
        status = data['status']
        try:
            bot_address = data['bot_address']
        except:
            bot_address = ''

        new_bot = {'bot_name' : bot_name,
                   'bot_user_name' : bot_user_name,
                   'token' : token,
                   'create_time' : create_time,
                   'owner' : owner,
                   'status' : status,
                   'bot_address' : bot_address}
        
        result = bot_hub.insert_one(new_bot)
        
        if result:
            response = {'code': 200, 'error': 'success'}
            return jsonify(response)
        else:
            response = {'code': 311, 'error': 'Add bot fail'}
            return jsonify(response)
    except Exception as e:
        response = {'code': 301, 'error': str(e)}
        return jsonify(response)
    

@app.route('/delete_bot', methods=['POST'])
def delete_bot():
    try:
        global db
        data = request.json
        token = data['token']
        bot_hub = db['bot_hub']
        search = bot_hub.find_one({'token': token})
        if search['status'] != '禁用':
            response = {'code': 350, 'error': 'can not delete un forbiden bot fail'}
            return jsonify(response)
        result = bot_hub.delete_many({'token': token})
        if result:
            response = {'code': 200, 'error': 'success'}
            return jsonify(response)
        else:
            response = {'code': 312, 'error': 'Delete bot fail'}
            return jsonify(response)
    except Exception as e:
        response = {'code': 302, 'error': str(e)}
        return jsonify(response)
    

@app.route('/edit_bot', methods=['POST'])
def edit_bot():
    try:
        global db
        data = request.json
        old_token = data['old_token']
        try:
            bot_name = data['bot_name']
        except:
            bot_name = ''
        bot_user_name = data['bot_user_name']
        token = data['token']
        try:
            bot_address = data['bot_address']
        except:
            bot_address = ''
        status = data['status']
        bot_hub = db['bot_hub']
        condition = {'token': old_token}
        output = bot_hub.find_one(condition)
        output['bot_name'] = bot_name
        output['bot_user_name'] = bot_user_name
        output['token'] = token
        output['bot_address'] = bot_address
        output['status'] = status
        setting = {"$set": output}
        result = bot_hub.update_many(condition, setting)
        if result:
            response = {'code': 200, 'error': 'success'}
            return jsonify(response)
        else:
            response = {'code': 313, 'error': 'Update bot fail'}
            return jsonify(response)
    except Exception as e:
        response = {'code': 314, 'error': str(e)}
        return jsonify(response)


@app.route('/ban', methods=['POST'])
def ban():
    try:
        global db
        data = request.json
        chat_id = data['chat_id']
        user_id = data['user_id']
        ban_time = data['ban_time']
        token = data['token']
        bot_hub = db['bot_hub']
        search = bot_hub.find_one({'token': token})
        if not search:
            response = {'code': 315, 'error': 'Bot not exist'}
            return jsonify(response)
        bot = Bot(token)
        # 禁言用户，时间单位为秒
        permissions = ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
        )
        bot.restrict_chat_member(chat_id, user_id, permissions, until_date=int(time.time())+int(ban_time))
        response = {'code': 200, 'error': 'success'}
        return jsonify(response)
    except Exception as e:
        response = {'code': 303, 'error': str(e)}
        return jsonify(response)
    

@app.route('/unban', methods=['POST'])
def unban():
    try:
        data = request.json
        chat_id = data['chat_id']
        user_id = data['user_id']
        token = data['token']
        global db
        bot_hub = db['bot_hub']
        search = bot_hub.find_one({'token': token})
        if not search:
            response = {'code': 315, 'error': 'Bot not exist'}
            return jsonify(response)
        bot = Bot(token)
        # 禁言用户，时间单位为秒
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True,
        )
        bot.restrict_chat_member(chat_id, user_id, permissions)
        response = {'code': 200, 'error': 'success'}
        return jsonify(response)
    except Exception as e:
        response = {'code': 304, 'error': str(e)}
        return jsonify(response)
    

@app.route('/kick', methods=['POST'])
def kick():
    try:
        data = request.json
        chat_id = data['chat_id']
        user_id = data['user_id']
        token = data['token']
        global db
        bot_hub = db['bot_hub']
        search = bot_hub.find_one({'token': token})
        if not search:
            response = {'code': 315, 'error': 'Bot not exist'}
            return jsonify(response)
        bot = Bot(token)
        bot.kick_chat_member(chat_id, user_id)
        response = {'code': 200, 'error': 'success'}
        return jsonify(response)
    except Exception as e:
        response = {'code': 305, 'error': str(e)}
        return jsonify(response)


@app.route('/set_group_name_description', methods=['POST'])
def set_group_name_description():
    try:
        data = request.json
        chat_id = data['chat_id']
        new_name = data['new_group_name']  # Replace with your desired group name
        new_description = data['new_group_description']
        token = data['token']
        global db
        bot_hub = db['bot_hub']
        group_hub = db['group_hub']
        search = bot_hub.find_one({'token': token})
        if not search:
            response = {'code': 315, 'error': 'Bot not exist'}
            return jsonify(response)
        bot = Bot(token)
        # Set new group name
        bot.set_chat_title(chat_id, new_name)
        try:
            bot.set_chat_description(chat_id, new_description)
        except Exception as e:
            if 'modified' in str(e):
                pass
            else:
                response = {'code': 339, 'error': str(e)}
                return jsonify(response)
        filter_condition = {"chat_id": chat_id}
        update_data = {
                        "$set": {
                                "title": new_name,
                                "description": new_description
                                }
                    }
        result = group_hub.update_one(filter_condition, update_data)
        response = {'code': 200, 'error': 'success'}
        return jsonify(response)
    except Exception as e:
        response = {'code': 306, 'error': str(e)}
        return jsonify(response)


@app.route('/list_bot', methods=['POST'])
def list_bot():
    try:
        global db
        bot_hub = db['bot_hub']
        searches = bot_hub.find()
        output = []
        for i in searches:
            t = {
                'bot_name' : i['bot_name'],
                'bot_user_name' : i['bot_user_name'],
                'token' : i['token'],
                'create_time' : i['create_time'],
                'owner' : i['owner'],
                'bot_address' : i['bot_address'],
                'status' : i['status']
            }
            output.append(t)
        response = {'code': 200, 'error': 'success', 'bot_list': output}
        return jsonify(response)
    except Exception as e:
        response = {'code': 308, 'error': str(e)}
        return jsonify(response)
    

@app.route('/group_info', methods=['POST'])
def group_info():
    try:
        data = request.json
        token = data['token']
        global db
        bot_hub = db['bot_hub']
        group_hub = db['group_hub']
        search = bot_hub.find_one({'token': token})
        if not search:
            response = {'code': 315, 'error': 'Bot not exist'}
            return jsonify(response)
        bot = Bot(token)
        updates = bot.get_updates()
        group_chat_ids = list(set([update.message.chat_id for update in updates if update.message and update.message.chat.type == 'supergroup']))
        output = []
        for chat_id in group_chat_ids:
            # Get information about the chat (group)
            query = {"chat_id": chat_id}
            chat_info = bot.get_chat(chat_id)

            # Access title and description from the chat_info object
            group_title = str(chat_info.title)
            group_description = str(chat_info.description)
            group_type = str(chat_info.type)
            member_count = str(bot.get_chat_member_count(chat_id))
            admin_list = []
            admin = bot.get_chat_administrators(chat_id=chat_id)
            random_number = 'G'+''.join([str(random.randrange(10)) for _ in range(11)])
            for i in admin:
                admin_list.append(i.to_dict())
            t = {'title':group_title, 
                 'description':group_description,
                 'type':group_type,
                 'member_count':member_count,
                 'token':token,
                 'chat_id':chat_id,
                 'group_index':random_number
            }
            update_data = {"$set": t}
            group_hub.update_many(query, update_data, upsert=True)
            output.append(t)

        response = {'code': 200, 'error': 'success', 'result': output}
        return jsonify(response)

    except Exception as e:
        response = {'code': 309, 'error': str(e)}
        return jsonify(response)
    

@app.route('/list_group', methods=['POST'])
def list_group():
    try:
        global db
        bot_hub = db['bot_hub']
        searches = bot_hub.find()
        output = []
        group_hub = db['group_hub']
        output = []
        for i in searches:
            token = i['token']
            bot = Bot(token)
            updates = bot.get_updates()
            group_chat_ids = list(set([update.message.chat_id for update in updates if update.message and update.message.chat.type == 'supergroup']))
            for chat_id in group_chat_ids:
                # Get information about the chat (group)
                query = {"chat_id": chat_id}
                chat_info = bot.get_chat(chat_id)

                # Access title and description from the chat_info object
                group_title = str(chat_info.title)
                group_description = str(chat_info.description)
                group_type = str(chat_info.type)
                member_count = str(bot.get_chat_member_count(chat_id))
                admin_list = []
                admin = bot.get_chat_administrators(chat_id=chat_id)
                for j in admin:
                    admin_list.append(j.to_dict())
                
                t = {
                    'title':group_title,
                    'description':group_description,
                    'type':group_type,
                    'member_count':member_count,
                    'chat_id':chat_id,
                    'token':token
                }
                update_data = {"$set": t}
                group_hub.update_many(query, update_data, upsert=True)
                t['group_index'] = group_hub.find_one(query).get('group_index')
                output.append(t)
            if group_hub.count_documents({}) > len(output):
                output = []
                searches = group_hub.find()
                for i in searches:
                    t = {
                    'title':i['title'],
                    'description':i['description'],
                    'type':i['type'],
                    'member_count':i['member_count'],
                    'chat_id':i['chat_id'],
                    'token':i['token'],
                    'group_index':i['group_index']
                    }
        response = {'code': 200, 'error': 'success', 'group_list': output}
        return jsonify(response)
    except Exception as e:
        response = {'code': 307, 'error': str(e), 'group_list': []}
        return jsonify(response)
    

@app.route('/member_info', methods=['POST'])
def member_info():
    try:
        data = request.json
        token = data['token']
        global db
        bot_hub = db['bot_hub']
        search = bot_hub.find_one({'token': token})
        if not search:
            response = {'code': 315, 'error': 'Bot not exist'}
            return jsonify(response)
        bot = Bot(token)
        chat_id = data['chat_id']
        admin_list = []
        admin = bot.get_chat_administrators(chat_id=chat_id)
        for i in admin:
            admin_list.append(i.to_dict())
        response = {'code': 200, 'error': 'success', 'result': admin_list}
        return jsonify(response)
    except Exception as e:
        response = {'code': 328, 'error': str(e), 'result':[]}
        return jsonify(response)
    

@app.route('/add_template', methods=['POST'])
def add_template():
    try:
        global db
        template_bub = db['template_bub']
        data = request.json
        template_name = data['template_name']
        search = template_bub.find_one({'template_name': template_name})
        if search:
            response = {'code': 317, 'error': 'Template already created!'}
            return jsonify(response)
        description = data['description']
        template = data['template']
        template_html = data['template_html']
        create_time = data['create_time']
        owner = data['owner']
        status = data['status']
        template_id = ''.join([str(random.randrange(10)) for _ in range(12)])
        new_template = {
            'template_name':template_name,
            'description':description,
            'template':template,
            'template_html':template_html,
            'create_time':create_time,
            'owner':owner,
            'status':status,
            'template_id':template_id
        }
        result = template_bub.insert_one(new_template)
        
        if result:
            response = {'code': 200, 'error': 'success'}
            return jsonify(response)
        else:
            response = {'code': 318, 'error': 'Add template fail'}
            return jsonify(response)

    except Exception as e:
        response = {'code': 316, 'error': str(e)}
        return jsonify(response)
    

@app.route('/show_template', methods=['POST'])
def show_template():
    try:
        global db
        template_bub = db['template_bub']
        data = request.json
        template_id = data['template_id']
        condition = {'template_id': template_id}
        search = template_bub.find_one(condition)
        if not search:
            response = {'code': 319, 'error': 'Template does not exist!', 'template':{}}
            return jsonify(response)
        output = template_bub.find_one(condition)
        old_template = {
            'template_name':output['template_name'],
            'description':output['description'],
            'template':output['template'],
            'template_html':output['template_html'],
            'status':output['status'],
            'template_id':output['template_id']
        }
        response = {'code': 200, 'error': 'success', 'template':old_template}
        return jsonify(response)
    except Exception as e:
        response = {'code': 320, 'error': str(e)}
        return jsonify(response)
    

@app.route('/edit_template', methods=['POST'])
def edit_template():
    try:
        global db
        template_bub = db['template_bub']
        data = request.json
        template_id = data['template_id']
        condition = {'template_id': template_id}
        search = template_bub.find_one(condition)
        if not search:
            response = {'code': 319, 'error': 'Template does not exist!'}
            return jsonify(response)
        new_name = data['template_name']
        description = data['description']
        template = data['template']
        template_html = data['template_html']
        status = data['status']
        search['template_name'] = new_name
        search['description'] = description
        search['template'] = template
        search['template_html'] = template_html
        search['status'] = status
        setting = {"$set": search}
        result = template_bub.update_many(condition, setting)
        if result:
            response = {'code': 200, 'error': 'success'}
            return jsonify(response)
        else:
            response = {'code': 321, 'error': 'Update template fail'}
            return jsonify(response)
    except Exception as e:
        response = {'code': 322, 'error': str(e)}
        return jsonify(response)


@app.route('/delete_template', methods=['POST'])
def delete_template():
    try:
        global db
        template_bub = db['template_bub']
        data = request.json
        template_id = data['template_id']
        search = template_bub.find_one({'template_id': template_id})
        if not search:
            response = {'code': 323, 'error': 'Template does not exist!'}
            return jsonify(response)
        if search['status'] != '禁用':
            response = {'code': 338, 'error': 'Only disable template can be deleted!'}
            return jsonify(response)
        result = template_bub.delete_many({'template_id': template_id})
        if result:
            response = {'code': 200, 'error': 'success'}
            return jsonify(response)
        else:
            response = {'code': 324, 'error': 'Delete template fail'}
            return jsonify(response)
    except Exception as e:
        response = {'code': 325, 'error': str(e)}
        return jsonify(response)
    

@app.route('/list_template', methods=['POST'])
def list_template():
    try:
        global db
        template_bub = db['template_bub']
        searches = template_bub.find()
        output = []
        for i in searches:
            t = {
                'template_name':i['template_name'],
                'description':i['description'],
                'template':i['template'],
                'template_html':i['template_html'],
                'create_time':i['create_time'],
                'owner':i['owner'],
                'status':i['status'],
                'template_id':i['template_id']
            }
            output.append(t)
        response = {'code': 200, 'error': 'success', 'template_list': output}
        return jsonify(response)
    except Exception as e:
        response = {'code': 326, 'error': str(e), 'template_list': []}
        return jsonify(response)
    

@app.route('/search_message', methods=['POST'])
def search_message():
    try:
        global db
        message_bub = db['message_hub']
        template_hub = db['template_bub']
        data = request.json
        try:
            message_name = data['message_name']
        except:
            message_name = ''
        try:
            template = data['template']
        except:
            template = ''
        try:
            status = data['status']
        except:
            status = ''
        condition = {}
        if message_name:
            condition['message_name'] = { '$regex' : message_name, '$options': "i" }
        if template:
            condition['template'] = template
        if status:
            condition['status'] = status
        search = message_bub.find(condition)
        output = []
        for i in search:
            t = {
                'message_id':i['message_id'],
                'message_name':i['message_name'],
                'template':i['template'],
                'owner':i['owner'],
                'schedule':i['schedule'],
                'method':i['method'],
                'create_time':i['create_time'],
                'send_time':i['send_time'],
                'end_time':i['end_time'],
                'delete_time':i['delete_time'],
                'send_groups':i['send_groups'],
                'status':i['status'],
                'template_name':''
                #'button':i['button'],
                #'message_content':i['message_content']
            }
            if i['template']:
                t['template_name'] = template_hub.find_one({'template_id':str(i['template'])})['template']
            output.append(t)
        response = {'code': 200, 'error': 'success', 'result':output}
        return jsonify(response)
    except Exception as e:
        response = {'code': 327, 'error': str(e), 'result':[]}
        return jsonify(response)


@app.route('/preview_message', methods=['POST'])
def preview_message():
    try:
        global db, preview_code_list
        bot_hub = db['bot_hub']
        group_hub = db['group_hub']
        data = request.json

        message_content = data['message_content']
        button = data['button']
        
        chat_id = data['chat_id']
        search = group_hub.find_one({'chat_id': chat_id})
        if not search:
            response = {'code': 350, 'error': 'group not found', 'result': ''}
            return jsonify(response)
        token = search['token']

        search = bot_hub.find_one({'token': token})
        if not search:
            response = {'code': 333, 'error': 'bot not found', 'result': ''}
            return jsonify(response)
        bot_name = search['bot_name']

        preview_code_t = ''.join([str(random.randrange(10)) for _ in range(6)])

        while preview_code_list not in preview_code_list:
            preview_code_t = ''.join([str(random.randrange(10)) for _ in range(6)])

        preview_code_list.append(preview_code_t)

        worker_process = multiprocessing.Process(target=preview_message_worker, args=(token, preview_code_t, message_content, button,))

        worker_process.start()
        result = {'code': preview_code_t, 'bot_name':bot_name}
        response = {'code': 200, 'error': 'success', 'result': result}
        return jsonify(response)
    except Exception as e:
        response = {'code': 329, 'error': str(e), 'result': ''}
        return jsonify(response)


@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        global db
        message_hub = db['message_hub']
        group_hub = db['group_hub']
        data = request.json
        
        message_name = data['message_name']
        template = data['template']
        owner = data['owner']

        schedule = data['schedule']
        
        message_content = data['message_content']
        button = data['button']
        
        create_time = data['create_time']
        delete_time = data['delete_time']
        if not delete_time:
            delete_time = -1
        send_time = data['send_time']
        
        send_groups = data['send_groups']

        message_id = ''.join([str(random.randrange(10)) for _ in range(12)])

        chat_bot_match = {}

        for group in send_groups:
            chat_id = group_hub.find_one({'title': group})['chat_id']
            token = group_hub.find_one({'title': group})['token']
            chat_bot_match[chat_id] = token

        worker_process = multiprocessing.Process(target=send_message_worker,args=(message_id, chat_bot_match, message_content, button, send_time, schedule, delete_time,))
        
        worker_process.start()

        worker_hub[message_id] = worker_process
        #print(worker_hub)

        response = {'code': 200, 'error': 'success'}
        if time.time() >= send_time:
            method = 'rightnow'
        else:
            method = 'schedule'
        in_db = {
            'message_id': message_id,
            'message_name': message_name,
            'template': template,
            'owner': owner,
            'schedule': schedule,
            'method': method,
            'create_time': create_time,
            'send_time': send_time,
            'end_time': send_time,
            'delete_time': delete_time,
            'send_groups': send_groups
        }
        if send_time <= time.time():
            in_db['status'] = '已发送'
        else:
            in_db['status'] = '待发送'
        result = message_hub.insert_one(in_db)
        return jsonify(response)
    except Exception as e:
        response = {'code': 334, 'error': str(e)}
        return jsonify(response)
    

@app.route('/kill_message', methods=['POST'])
def kill_message():
    data = request.json
    global worker_hub
    global db
    message_hub = db['message_hub']
    message_id = data['message_id']
    try:
        worker = worker_hub[message_id]
        worker.terminate()
    except:
        pass

    try:
        condition = {"message_id": message_id}
        update_data = {"$set": {"status": "已取消", "end_time":int(time.time())}}
        message_hub.update_one(condition, update_data)
        response = {'code': 200, 'error': 'success'}
        return jsonify(response)
    except Exception as e:
        response = {'code': 335, 'error': str(e)}
        return jsonify(response)
    

@app.route('/delete_message', methods=['POST'])
def delete_message():
    try:
        data = request.json
        global db
        message_hub = db['message_hub']
        message_id = data['message_id']
        search = message_hub.find_one({'message_id': message_id})
        if not search:
            response = {'code': 340, 'error': 'Message does not exist!'}
            return jsonify(response)
        if search['status'] != '已发送' and search['status'] != '已取消':
            response = {'code': 341, 'error': 'Only sent or canceled message can be deleted!'}
            return jsonify(response)
        result = message_hub.delete_many({'message_id': message_id})
        if result:
            response = {'code': 200, 'error': 'success'}
            return jsonify(response)
        else:
            response = {'code': 342, 'error': 'Delete message fail'}
            return jsonify(response)
    except Exception as e:
        response = {'code': 343, 'error': str(e)}
        return jsonify(response)
    

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_name = data['user_name']
    password = data['password']
    cap = str(data['captcha'])
    global db, captcha_save
    user_hub = db['user_hub']
    search = user_hub.find_one({'user_name': user_name, 'password': password})
    if search:
        if cap.upper() == captcha_save.upper():
            response = {'code': 200, 'error': 'success', 'isAdmin': search['isAdmin']}
        else:
            response = {'code': 336, 'error': 'captcha error!'}
    else:
        response = {'code': 331, 'error': 'user name or password incorrect!'}
    
    return jsonify(response)
    

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user_name = data['user_name']
    password = data['password']
    isAdmin = data['isAdmin']
    status = data['status']
    id = ''.join([str(random.randrange(10)) for _ in range(12)])
    global db
    user_hub = db['user_hub']
    if user_hub.find_one({'user_name': user_name}):
        response = {'code': 332, 'error': 'user name exist!'}
        return jsonify(response)
    user_hub.insert_one({'user_name': user_name, 'password': password, 'isAdmin': isAdmin, 'status': status, 'id':id})
    response = {'code': 200, 'error': 'success'}

    return jsonify(response)


@app.route('/captcha')
def captcha():
    chr_all = string.ascii_letters + string.digits
    global captcha_save
    captcha_save = ''.join(random.sample(chr_all, 4))
    image = ImageCaptcha().generate_image(captcha_save)

    buf = io.BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)
    return buf.getvalue(), 200, {
        'Content-Type': 'image/png',
        'Content-Length': str(len(buf.getvalue()))
    }


@app.route('/list_user')
def list_user():
    try:
        global db
        user_hub = db['user_hub']
        searches = user_hub.find()
        output = []
        for i in searches:
            t = {
                'user_name' : i['user_name'],
                'status' : i['status'],
                'id' : i['id']
                }
            output.append(t)
        response = {'code': 200, 'error': 'success', 'user_list': output}
        return jsonify(response)
    except Exception as e:
        response = {'code': 308, 'error': str(e)}
        return jsonify(response)
    

@app.route('/edit_user', methods=['POST'])
def edit_user():
    try:
        global db
        user_hub = db['user_hub']
        data = request.json
        id = data['id']
        user_name = data['user_name']
        password = data['password']
        isAdmin = data['isAdmin']
        status = data['status']
        if isAdmin == 'True':
            response = {'code': 344, 'error': 'can not edit super admin'}
            return jsonify(response)

        condition = {'id': id}
        output = user_hub.find_one(condition)
        output['user_name'] = user_name
        output['password'] = password
        output['status'] = status
        setting = {"$set": output}
        result = user_hub.update_many(condition, setting)
        if result:
            response = {'code': 200, 'error': 'success'}
            return jsonify(response)
        else:
            response = {'code': 345, 'error': 'Update user fail'}
            return jsonify(response)
    except Exception as e:
        response = {'code': 346, 'error': str(e)}
        return jsonify(response)
    

@app.route('/delete_user', methods=['POST'])
def delete_user():
    try:
        global db
        data = request.json
        id = data['id']
        isAdmin = data['isAdmin']
        if isAdmin == 'True':
            response = {'code': 347, 'error': 'can not delete super admin'}
            return jsonify(response)
        user_hub = db['user_hub']

        result = user_hub.delete_many({'id': id})
        if result:
            response = {'code': 200, 'error': 'success'}
            return jsonify(response)
        else:
            response = {'code': 348, 'error': 'Delete user fail'}
            return jsonify(response)
    except Exception as e:
        response = {'code': 349, 'error': str(e)}
        return jsonify(response)


if __name__ == '__main__':
    ip = '0.0.0.0'
    port = '5000'
    app.run(host=ip, port=port)

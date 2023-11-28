from flask import Flask, request, jsonify
from telegram import Bot, ChatPermissions
import time
import json
import pymongo


app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

db_client = pymongo.MongoClient(host='localhost', port=27017)

db = db_client['telegram']

# health check
@app.route('/health', methods=['GET'])
def health_check():
    return 'OK', 200


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
        bot_name = data['bot_name']
        bot_user_name = data['bot_user_name']
        create_time = data['create_time']
        owner = data['owner']
        bot_address = data['bot_address']

        new_bot = {'bot_name' : bot_name,
                   'bot_user_name' : bot_user_name,
                   'token' : token,
                   'create_time' : create_time,
                   'owner' : owner,
                   'bot_address' : bot_address}
        
        result = bot_hub.insert_one(new_bot)
        
        if result:
            response = {'code': 200, 'error': 'success'}
            return jsonify(response)
        else:
            response = {'code': 311, 'error': 'Add bot fail'}
            return jsonify(response)
    except Exception as e:
        response = {'code': 301, 'error': e}
        return jsonify(response)
    

@app.route('/delete_bot', methods=['POST'])
def delete_bot():
    try:
        global db
        data = request.json
        token = data['token']
        bot_hub = db['bot_hub']
        result = bot_hub.delete_many({'token': token})
        if result:
            response = {'code': 200, 'error': 'success'}
            return jsonify(response)
        else:
            response = {'code': 312, 'error': 'Delete bot fail'}
            return jsonify(response)
    except Exception as e:
        response = {'code': 302, 'error': e}
        return jsonify(response)
    

@app.route('/edit_bot', methods=['POST'])
def edit_bot():
    try:
        global db
        data = request.json
        old_token = data['old_token']
        bot_name = data['bot_name']
        bot_user_name = data['bot_user_name']
        token = data['token']
        bot_address = data['bot_address']
        bot_hub = db['bot_hub']
        condition = {'token': old_token}
        output = bot_hub.find_one(condition)
        output['bot_name'] = bot_name
        output['bot_user_name'] = bot_user_name
        output['token'] = token
        output['bot_address'] = bot_address
        setting = {"$set": output}
        result = bot_hub.update_many(condition, setting)
        if result:
            response = {'code': 200, 'error': 'success'}
            return jsonify(response)
        else:
            response = {'code': 313, 'error': 'Update bot fail'}
            return jsonify(response)
    except Exception as e:
        response = {'code': 314, 'error': e}
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
        response = {'code': 303, 'error': e}
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
        response = {'code': 304, 'error': e}
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
        response = {'code': 305, 'error': e}
        return jsonify(response)


@app.route('/set_group_name', methods=['POST'])
def set_group_name():
    try:
        data = request.json
        chat_id = data['chat_id']
        new_name = data['new_group_name']  # Replace with your desired group name
        token = data['token']
        global db
        bot_hub = db['bot_hub']
        search = bot_hub.find_one({'token': token})
        if not search:
            response = {'code': 315, 'error': 'Bot not exist'}
            return jsonify(response)
        bot = Bot(token)
        # Set new group name
        bot.set_chat_title(chat_id, new_name)
        response = {'code': 200, 'error': 'success'}
        return jsonify(response)
    except Exception as e:
        response = {'code': 306, 'error': e}
        return jsonify(response)


@app.route('/set_group_description', methods=['POST'])
def set_group_description():
    try:
        data = request.json
        chat_id = data['chat_id']
        new_description = data['new_group_description']  # Replace with your desired group description
        token = data['token']
        global db
        bot_hub = db['bot_hub']
        search = bot_hub.find_one({'token': token})
        if not search:
            response = {'code': 315, 'error': 'Bot not exist'}
            return jsonify(response)
        bot = Bot(token)
        # Set new group description
        bot.set_chat_description(chat_id, new_description)
        response = {'code': 200, 'error': 'success'}
        return jsonify(response)
    except Exception as e:
        response = {'code': 307, 'error': e}
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
                'bot_address' : i['bot_address']
            }
            output.append(t)
        response = {'code': 200, 'error': 'success', 'bot_list': output}
        return jsonify(response)
    except Exception as e:
        response = {'code': 308, 'error': e}
        return jsonify(response)
    

@app.route('/group_info', methods=['POST'])
def group_info():
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
        updates = bot.get_updates()
        group_chat_ids = list(set([update.message.chat_id for update in updates if update.message and update.message.chat.type == 'supergroup']))
        output = []
        for chat_id in group_chat_ids:
            # Get information about the chat (group)
            chat_info = bot.get_chat(chat_id)

            # Access title and description from the chat_info object
            group_title = str(chat_info.title)
            group_description = str(chat_info.description)
            group_type = str(chat_info.type)
            member_count = str(bot.get_chat_member_count(chat_id))
            admin_list = []
            admin = bot.get_chat_administrators(chat_id=chat_id)
            for i in admin:
                admin_list.append(i.to_dict())
            t = {'title':group_title, 
                 'description':group_description,
                 'type':group_type,
                 'member_count':member_count,
                 'admin':admin_list,
                 'chat_id':chat_id
                 }
            output.append(t)

        response = {'code': 200, 'error': 'success', 'result': output}
        return jsonify(response)

    except Exception as e:
        response = {'code': 309, 'error': e}
        return jsonify(response)


if __name__ == '__main__':
    ip = '0.0.0.0'
    port = '4000'
    app.run(host=ip, port=port)

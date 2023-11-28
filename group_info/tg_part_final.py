import json


from telethon.tl.types import PeerUser, PeerChat, PeerChannel,UpdateNewChannelMessage
from telethon.tl.types import ChannelParticipantsAdmins



async def tg_get_group_part(client,part_file_local,part_admin_file_local,channel_id,group_num):
    client = client
    result = [] #用于储存json文件
    result_admin = [] #用于储存json文件
    # ===============获取admin========
    for user in await client.get_participants(await client.get_entity(PeerChannel(int('{channel_id}'.format(channel_id=channel_id)))),filter=ChannelParticipantsAdmins, aggressive=True):
        temp_dict = {}
        temp_dict['admin_用户_id：'] = user.id
        temp_dict['admin_用户_first_name'] = user.first_name
        temp_dict['admin_用户_last_name'] = user.last_name
        temp_dict['admin_用户名_username'] = user.username
        temp_dict['admin_用户_phone'] = user.phone
        result_admin.append(temp_dict)
    print('===== 获取群管理员结束 ====')
    # try:
    #     with open('{file_local}'.format(file_local=part_admin_file_local),'w',encoding='utf-8') as f :
    #         json.dump(result_admin,f,ensure_ascii=False,indent=2)
    # except Exception as e:
    #     print(e.args)
    #     pass
        # print(user.stringify())

    # ===============获取群成员信息========
# =========获取用户id 1W+，同时可以获取用户内容==================
    channel =await client.get_entity(PeerChannel(int('{channel_id}'.format(channel_id=channel_id))))  # 根据群组id获取群组对
    # channel = '[公海總谷2.0] 五大訴求，缺一不可。'
    #两种channel都可以,人数少于1w的时候正常请求，多余1w 主动探测请求
    if(int(group_num) <= 10000):
        responses =client.iter_participants(channel)  # 获取群组所有用户信息
    else:
        responses = client.iter_participants(channel,aggressive=True)
    async for resp in responses:
        try:
            # print('用户id：',resp.id,'用户first_name',resp.first_name,'用户last_name',resp.last_name,'用户名 username',resp.username,'用户 phone',resp.phone)
            temp_dict = {}
            temp_dict['用户_id：'] = resp.id
            temp_dict['用户_first_name'] = resp.first_name
            temp_dict['用户_last_name'] = resp.last_name
            temp_dict['用户名_username'] = resp.username
            temp_dict['用户_phone'] = resp.phone
            result.append(temp_dict)
            print('part------------->',resp.id)

        except Exception as e:
            print(e.args)
            pass
    print('==== 获取群成员结束 ====')
    try:
        with open('{file_local}'.format(file_local=part_file_local), 'w', encoding='utf-8') as f:
            json.dump(result_admin, f, ensure_ascii=False, indent=2)
            json.dump(result, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(e.args)
        pass
# with client:
#     client.loop.run_until_complete(main())
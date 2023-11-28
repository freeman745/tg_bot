import json
import re

from telethon import TelegramClient
from telethon.tl import functions
from telethon.tl.types import PeerChannel

# api_id = config.api_id
# api_hash = config.api_hash


# 获取频道信息，名称，id 判断是否为channel   使用频道信息的 broadcast参数
async def tg_get_group_info(client,group_location):

    client = client
    file_local = group_location

    result_group_info = []
    async for dialog in client.iter_dialogs():
    # async for dialog in client.get_dialogs():
        dict_temp = {}
        # print(dialog.name, 'has ID', dialog.id)
        # print(dialog.stringify())
        #获取频道id  第二种方式#
        # print(await client.get_peer_id('草菇草菇caogu.tv'))
        # print(dialog.title,dialog.id)

    # 根据id 获取群组信息  信息很全面
        try:
            Chat_Full_Info = await client(           functions.channels.GetFullChannelRequest(
                channel=await client.get_entity(
                    PeerChannel(
                        int('{}'.format(dialog.id))
                    )
                )
            ))
        except Exception as e:
            # print("Chat_Full_Info",e.args)
            continue
        # print(Chat_Full_Info.chats[0].broadcast)
        try:
            # print("=============")
            if Chat_Full_Info.chats[0].broadcast == False:
                dict_temp['聊天组Group名：'] = Chat_Full_Info.chats[0].title
                dict_temp['组id：'] = Chat_Full_Info.chats[0].id
                dict_temp['组链接：'] = Chat_Full_Info.chats[0].username
                try:
                    dict_temp['群组简介：'] = Chat_Full_Info.full_chat.about
                except Exception as e:
                    print("聊天组Group_简介",e.args)
                    dict_temp['群组简介：'] = " "
                try:
                    dict_temp['群组总人数：'] = Chat_Full_Info.full_chat.participants_count
                except Exception as e:
                    print("群组总人数",e.args)
                    dict_temp['群组总人数：'] = " "


                # # 提取hex值 连接
                try:
                    dict_temp['hex链接：'] = re.match(r'(.*?)(https://t\.me/joinchat/[]a-zA-Z0-9_\-]{22})(.*?)',str(Chat_Full_Info.full_chat.about).replace('\r', '').replace('\n','').strip()).group(2)
                except Exception as e:
                    # print("hex链接",e.args)
                    dict_temp['hex链接：'] = ' '

                print("聊天组Group名：" + dialog.name, "，组id：-100"+str( dialog.entity.id))
                result_group_info.append(dict_temp)
            elif Chat_Full_Info.chats[0].broadcast == True:
                dict_temp['频道channel名：'] = Chat_Full_Info.chats[0].title
                dict_temp['频道id：'] = Chat_Full_Info.chats[0].id
                dict_temp['频道链接：'] = Chat_Full_Info.chats[0].username
                try:
                    dict_temp['频道简介：'] =Chat_Full_Info.full_chat.about
                except Exception as e:
                    print("频道简介：",e.args)
                    dict_temp['频道简介：'] = " "

                try:
                    dict_temp['频道总人数：'] = Chat_Full_Info.full_chat.participants_count
                except Exception as e:
                    print("频道总人数：",e.args)
                    dict_temp['频道总人数：'] = " "
                try:
                    dict_temp['hex链接：'] = re.match(r'(.*?)(https://t\.me/joinchat/[]a-zA-Z0-9_\-]{22})(.*?)',str(Chat_Full_Info.full_chat.about).replace('\r', '').replace('\n','').strip()).group(2)
                except Exception as e:
                    # print("hex链接：",e.args)
                    dict_temp['hex链接：'] = ' '
                result_group_info.append(dict_temp)
                print("频道channel名：" + dialog.name, "，频道id：-100" + str(dialog.entity.id))
            else:
                print("个人：", dialog.name)
        except Exception as e:
            print(e.args)
            # print("=============")
            # print("个人：", dialog.name)
            pass
            # 写入 json文件
    print("===== 获取群组信息结束 ========")
    try:
        with open("{local}".format(local=file_local), 'w', encoding='utf-8') as f:
            json.dump(result_group_info, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(e.args)
        pass

# with client:
#     client.loop.run_unChat_Full_Infotil_complete(tg_get_group_info_final())
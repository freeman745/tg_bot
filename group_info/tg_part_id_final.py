import json
import time
from telethon.tl import functions
from telethon.tl.types import PeerChannel, PeerUser

import client_config


#file_local:文件生成位置,
#file_to_read：需要读取的文件
async def getUserInfo_byId(client,file_to_read,file_local):
    tg_u = []
    temp_u = []  # 只存 用户id,方便去重
    # print('file_to_read',file_to_read,'file_local',file_local)
    try:
        with open(file_to_read,'r',encoding='utf-8') as load_f:
            tg_user = json.load(load_f)
            for i in range(0, len(tg_user)):
                temp_u.append(tg_user[i]['发言者ID：'])
                # tg_u_dict[tg_user[i]['发言者ID：']] = i + 1
            temp_u_format = list(set(temp_u))
            # print(temp_u_format)
            # print(tg_u_dict)
            # 获取发言者信息
        for i in range(0, len(temp_u_format)):
            tg_user_final = {}
            print('msg_part---------------->',temp_u_format[i])
            try:
                result_msg = await client.get_entity(PeerUser(int("{}".format(temp_u_format[i]))))
                # print(result_msg)
                tg_user_final['发言者id：'] = str(result_msg.id)
                tg_user_final['发言者first_name：'] = str(result_msg.first_name)
                tg_user_final['发言者last_name ：'] = str(result_msg.last_name)
                tg_user_final['发言者username ：'] = str(result_msg.username)
                tg_user_final['发言者phone ：'] = str(result_msg.phone)
                # print('tg_user_final[i]',tg_user_final)
                tg_u.append(tg_user_final)
                # print('tg_u----->', tg_u)
            except Exception as e:
                print('tg_u----->',e.args)
                pass
        # print('tg_u----->', tg_u)
        try:
            with open(file_local, 'w', encoding='utf-8') as f:
                json.dump(tg_u, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("写入by_id：", e.args)
    except Exception as e:
        print('file_to_read', e.args)
        pass
# s = time.time().

# with client:
#     client.loop.run_until_complete(main())
# print(time.time()-s)
# button_getUserInfo_byId(msg_file_local)
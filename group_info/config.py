import json
import os
import re

from telethon import TelegramClient
from telethon import TelegramClient, sync,events


from tel.tg_final import tg_msg_final
import tg_msg_final
import tg_get_group_info_final
import tg_group_part_info_final
import tg_add_group_final

##################  手动更改区域  ####################################
                                                                  ##
# ==============   +8615303517524    ===================          ##
api_id = 1188540                                                  ##
api_hash = 'f7fa2a4d485d3e1cb2177e74a2286589'                     ##
client = TelegramClient('8615303517524.session', api_id, api_hash)##
                                                                  ##
                                                                  ##
#=============== 群组信息存放位置，需要先确定群组信息存放位置=======     ##
group_location = 'E:\\group_info.json'                            ##
# group_location = 'E:\\group.txt'                                ##
                                                                  ##
#获取信息数量                                                       ##
msg_num = 1000                                                    ##
#控制开关 ，是否进行相应的函数调用  1：使用 0：不使用
                                                                   ##
button_part = 0 #获取群成员                                                                ##
button_msg = 1 #获取群聊天信息

#!!!!群信息，必须要获取一次之后才可以关闭， 否则群信息，群成员均无法获得！！！
button_group = 0 #获取群信息 #                                          ##
####################################################################


#===============  文件输出位置 创建对应的文件夹,以及文件==============
def mkdir(path):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", path)  # 替换为下划线
    # path = str(new_title).strip().replace()
    if not os.path.exists(new_title):
        os.makedirs('E:\\test!!!\\'+new_title)
    fp = open('E:\\\\test!!!\\\\'+new_title+'\\\\msg.json', 'w')
    fp1 = open('E:\\\\test!!!\\\\'+new_title+'\\\\part.json', 'w')
    fp2 = open('E:\\\\test!!!\\\\' + new_title + '\\\\part_admin.json', 'w')

#floder_name : 用组名称，创建文件夹
#group_id : 组id，用于获取聊天信息
def mkFIle_localtion(floder_name,group_id,group_name,group_num):
    file_local_list = []
    #创建文件夹
    try:
        mkdir(floder_name)
    except:
        pass
    print("mkFIle_localtion")
    file_msg_location = 'E:\\\\test!!!\\\\{floderLocation}\\\\msg.json'.format(floderLocation=floder_name)
    file_part_location = 'E:\\\\test!!!\\\\{floderLocation}\\\\part.json'.format(floderLocation=floder_name)
    file_part_admin_location = 'E:\\\\test!!!\\\\{floderLocation}\\\\part_admin.json'.format(floderLocation=floder_name)

    file_local_list.append(file_msg_location) #msg文件位置
    file_local_list.append(file_part_location) #part文件位置
    file_local_list.append(file_part_admin_location)  # part文件位置
    file_local_list.append(group_id) # 组id
    file_local_list.append(group_name) # 组名
    file_local_list.append(group_num)  # 组成员人数
    return  file_local_list

# ============  主程序运行   ================

with client:
    #用于储存所有 文件夹名称 同时列表也存在 文件名称 群成员.json 群信息.json
    file_total_list = []

    # 获取群组信息，并存放在指定位置
    if(int(button_group) == 1):
        try:
            client.loop.run_until_complete(tg_get_group_info_final.tg_get_group_info())
        except:
            pass

    #通过获取的群组信息，进行内容，群成员获取
    try:
        with open('{}'.format(group_location), 'r', encoding='utf-8') as f:
            result = json.loads(f.read())
            # print(result[0]['频道channel名：'])
            for i in range(0, len(result)):
                try:
                    if (str(result[i]).find('聊天组Group名：')) > 0:
                        local = mkFIle_localtion(result[i]['聊天组Group名：'],result[i]['组id：'],result[i]['聊天组Group名：'],result[i]['群组总人数：'])
                        file_total_list.append(local)
                    else:
                        # print('频道channel名：',result[i]['频道channel名：'],result[i]['频道id：'])
                        local = mkFIle_localtion(result[i]['频道channel名：'],result[i]['频道id：'],result[i]['频道channel名：'],result[i]['频道总人数：'])
                        file_total_list.append(local)
                except Exception as e:
                    print('将内容合并：',e.args)
                    pass
    except Exception as e:
        print('获取的群组信息：',e.args)
        pass

#获取 群、频道 聊天信息内容，群成员
    # file_total_list[i][0]：msg文件位置
    # file_total_list[i][1]：part文件位置
    # file_total_list[i][2]：part_admin文件位置
    # file_total_list[i][3]：group/channel id
    # file_total_list[i][4]：group/channel name
    # file_total_list[i][5]：group/channel 总人数
    for i  in range(0,len(file_total_list)):
        if(int(button_part) == 1):
            try:
                client.loop.run_until_complete(tg_group_part_info_final.tg_get_group_part(file_total_list[i][1],file_total_list[i][2],file_total_list[i][3],file_total_list[i][5]))
            except Exception as e:
                print("tg_get_group_part",e.args)
                pass
        if(int(button_msg) == 1):
            try:
                # print(file_total_list[i][1],file_total_list[i][2])
                client.loop.run_until_complete(tg_msg_final.tg_msg(file_total_list[i][0],file_total_list[i][3]))
            except Exception as e:
                print("tg_msg",e.args)
                pass
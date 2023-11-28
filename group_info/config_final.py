import datetime
import json
import os
import re

import tg_part_id_final
import tg_group_final
import tg_part_final
import tg_msg_final
import client_config

##################  手动更改区域  #####################################################

#文件储存路径为 例如： root_floder\电报账户\tg组名\msg.json
root_floder = 'tmp/'
# 获取聊天信息数量
msg_num = 0
#从何时起，向后（例如：2019-11-04 ---> 2019-11-05）获取 msg——num条信息
msg_date = datetime.date(2019,11,4)
    # 控制开关  【1：使用此函数 0：不使用】
# 获取群信息
button_group = 1
# 获取群成员
button_part = 1
# 获取群信息
button_msg = 0 # 获取群聊天信息
#button_getUserInfo_byId 打开速度很慢，【建议前三项获取之后，关闭前三项，再开启这个开关】
#此函数 依赖 button_msg 函数产生的msg.jso文件，故必须先将button_msg运行一次，或者二者同时运行
button_getUserInfo_byId = 0 #获取成员信息通过 聊天信息的 id  速度：300分/10000 id

###################################################################################


#文件输出位置 创建对应的文件夹,以及文件
#floder_name :文件夹名称
#account_floder : 账户
#file_type：msg、 msg_user、 part、group
def mkdir(account_floder,floder_name,file_type):
    rstr = r"[\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    floder_name = re.sub(rstr, "_", floder_name)  # 替换为下划线
    path = root_floder + account_floder + "\\\\" + floder_name
    file_need_make = path+'\\\\'+'{}.json'.format(file_type)
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path):
        with open(file_need_make, 'w', encoding='utf-8') as ff:
            print(file_need_make, '创建成功')
    return file_need_make

# acount_floder_name  :用账户名 创建文件夹
# floder_name : 用组名称，创建文件夹
# group_id : 组id，用于获取聊天信息
def mkFIle_localtion(acount_floder_name,floder_name, group_id, group_name, group_num):
    file_local_list = []
    # 创建文件夹
    rstr = r"[\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    count_floder_title = re.sub(rstr, "_", acount_floder_name)  # 替换为下划线
    group_floder_title = re.sub(rstr, "_", floder_name)  # 替换为下划线
    msg_json = ' '
    # msg_user msg_user 文件的位置
    msg_user_json = ' '
    # part part 文件的位置
    part_json = ' '
    file_msg_location = msg_json
    file_part_location = part_json
    file_msg_user_location = msg_user_json
    file_part_admin_location = ' '
    file_local_list.append(file_msg_location)  # msg文件位置
    file_local_list.append(file_part_location)  # part文件位置
    file_local_list.append(file_part_admin_location)  # part文件位置
    file_local_list.append(group_id)  # 组id
    file_local_list.append(group_name)  # 组名
    file_local_list.append(group_num)  # 组成员人数
    file_local_list.append(file_msg_user_location)  # msg 中人员信息文件

    # print("\n---》mkFIle_localtion《---\n")
    return file_local_list


# ============  主程序运行   ================
def run(clientList):
    for clitn_i in clientList:
        client = clitn_i
        with client:
            print(client.get_me().first_name)
            print(client.get_me().last_name)
            print(client.get_me().phone)
            username = str(client.get_me().first_name)+'_'+str(client.get_me().phone)
            # 用于储存所有 文件夹名称 同时列表也存在 文件名称 群成员.json 群信息.json
            file_total_list = []
            #获取 group信息 文件路径
            group_file_path = mkdir(username,'group_info','group_info')
            # 获取群组信息，并存放在指定位置
            if int(button_group) == 1:
                # group/channel 信息文件 位置

                print('用户 ---》', username,' 获取群信息')
                try:
                    client.loop.run_until_complete(tg_group_final.tg_get_group_info(client,group_file_path))
                except Exception as e:
                    print('tg_get_group_info',e.args)
                    pass
                print('！！！群信息写入结束！！！')
            # 通过获取的群组信息，进行内容，群成员获取
            try:
                with open('{}'.format(group_file_path), 'r', encoding='utf-8') as f:
                    result = json.loads(f.read())
                    # print(result[0]['频道channel名：'])
                    for i in range(0, len(result)):
                        try:
                            if (str(result[i]).find('聊天组Group名：')) > 0:
                                count = client.get_me().first_name
                                local = mkFIle_localtion(count,result[i]['聊天组Group名：'], result[i]['组id：'],result[i]['聊天组Group名：'], result[i]['群组总人数：'])
                                file_total_list.append(local)
                            else:
                                # "此处，如果是需要channel 的话，可以吧pass注释，下面的代码激活"
                                
                                count = client.get_me().first_name
                                # # print('频道channel名：',result[i]['频道channel名：'],result[i]['频道id：'])
                                local = mkFIle_localtion(count,result[i]['频道channel名：'], result[i]['频道id：'],
                                                         result[i]['频道channel名：'], result[i]['频道总人数：'])
                                file_total_list.append(local)
                        except Exception as e:
                            print('将内容合并：', e)
                            pass
            except Exception as e:
                print('获取的群组信息：', e.args)
                pass

            # 获取 群、频道 聊天信息内容，群成员
            # file_total_list[i][0]：空（msg文件位置）
            # file_total_list[i][1]：空（part文件位置）
            # file_total_list[i][2]：空
            # file_total_list[i][3]：group/channel id
            # file_total_list[i][4]：group/channel name
            # file_total_list[i][5]：group/channel 总人数
            # file_total_list[i][6]：空 （msg 中人员信息文件）
            for i in range(0, len(file_total_list)):
                # 获取 群成员信息
                if int(button_part) == 1:
                    # part 信息文件 位置
                    group_part_path = mkdir(username,file_total_list[i][4],'part')

                    print('用户 ---》', username, " 获取群成员")
                    try:
                        print('群组---》',file_total_list[i][4])
                        client.loop.run_until_complete(
                            tg_part_final.tg_get_group_part(client,group_part_path, file_total_list[i][2],file_total_list[i][3], file_total_list[i][5]))
                    except Exception as e:
                        print("tg_get_group_part", e.args)
                        pass
                    print('！！！群成员写入结束！！！')
                # 获取群聊天信息
                if int(button_msg) == 1:
                    # msg 信息文件 位置
                    group_msg_path = mkdir(username,file_total_list[i][4],'msg')

                    print('用户---》', username," 获取聊天信息")
                    try:
                        print('群组---》', file_total_list[i][4])
                        # print(file_total_list[i][1],file_total_list[i][2])
                        client.loop.run_until_complete(
                            tg_msg_final.tg_msg(client,msg_num,group_msg_path, file_total_list[i][3],msg_date))
                    except Exception as e:
                        print("tg_msg", e.args)
                        pass
                    print('！！！聊天信息写入结束！！！')
                #通过群消息获取用户 信息
                if int(button_getUserInfo_byId) == 1:
                    # msg_user msg_user 文件的位置
                    group_msg_path = mkdir(username, file_total_list[i][4], 'msg')
                    group_msg_user_path = mkdir(username, file_total_list[i][4], 'msg_user')
                    print('用户 ---》', username, " 获取聊天信息群成员")
                    try:
                        print('群组---》', file_total_list[i][4])
                        client.loop.run_until_complete(tg_part_id_final.getUserInfo_byId(client,group_msg_path,group_msg_user_path))
                    except Exception as e:
                        print("tg_msg_user", e.args)
                        pass
                    print('！！！聊天信息群成员更新结束！！！')

run(client_config.client_list)

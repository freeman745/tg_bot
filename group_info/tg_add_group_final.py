import re
import time

import client_config
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

#===============全局变量区域===============
group_temp_result=[] #临时储存结果
group_final_joinchat_result= [] #加入到joinchat 邀请群
group_final_result=[] #加入到公开的群



#总共多少个账户
# =======================================
#未加群的文件
file_local = 'D:\我的\工作\知道创宇\任务\电报\\未加群.txt'

#客户列表。需要手动添加
client_list_group = []

for i in client_config.client_list:
    client_list_group.append(i)
total_account=len(client_config.client_list)
# ================================================

#获得群组链接，把群组链接区分，加入到对应的列表中
def get_group_list():
    global group_final_joinchat_result
    global group_final_result
    with open('{file_local}'.format(file_local=file_local),'r',encoding='utf-8') as file:
        for f in file.readlines():
            group_temp_result.append(f)
    for resu in group_temp_result:
        patr = re.split(r'/',resu)
        if len(patr)==3: #私人链接
            group_final_joinchat_result.append(patr[2].replace('\n',''))
        if len(patr)==2: #公开链接
            group_final_result.append(str(resu).replace('\n',''))

# 第几个用户开始添加
async def main(client_i):
    print("用户{}开始：==========".format(client_i+1))

    joinchat_step = int(len(group_final_joinchat_result)/total_account)
    step = int(len(group_final_result)/total_account)
    print('每个用户添加的私人群组：',joinchat_step,'每个用户添加的公开群组：',step)

    #添加成功的总数
    step_num = 0
    joinchat_step_num = 0
    # ================自动添加公开群组====================
    for i in range(0, step):
        time.sleep(20)  # 每隔20秒加群
        print('第 {group_id} 个公开链接 {link} ---> '.format(group_id=i + step * int(client_i),link = group_final_result[i + step * int(client_i)]))
        try:
            await client_list_group[client_i](JoinChannelRequest('https://{}'.format(group_final_result[i+ step * int(client_i)])))
            print("【用户{}】 加群成功：--->".format(client_i+1) + str(group_final_result[i]))
            step_num += 1
        except Exception as e:
            print("【用户{}】 加群失败：--->".format(client_i+1) + str(group_final_result[i]))
            # print(e.args[0])
    print("【用户{}】 成功：--->{step_num}个公开群组".format(client_i+1,step_num=step_num))
    for i in range(0,joinchat_step):
        time.sleep(60)  # 每隔60秒加群

        print('第 {group_id} 个私人链接 {link}---> '.format(group_id = i+joinchat_step*int(client_i) , link =group_final_joinchat_result[i+joinchat_step*int(client_i)]))
        try:
            # time.sleep(20)
            updates1 = await client_list_group[client_i](ImportChatInviteRequest('{}'.format(group_final_joinchat_result[i+joinchat_step*int(client_i)])))
            # print('updates1',updates1)
            print("【用户{}】私人链接加入成功：--->".format(client_i+1) + str(group_final_joinchat_result[i]))
            joinchat_step_num += 1
            #如果添加成功5个群，则会暂停 1300s
            if (joinchat_step_num%5 ==0):
                time.sleep(1300)
        except Exception as e:
            print("【用户{}】私人链接加入失败：--->".format(client_i+1) + str(group_final_joinchat_result[i]))
            print(e.args)
    print("【用户{}】 成功：--->{joinchat_step_num}个公开群组".format(client_i + 1, joinchat_step_num=joinchat_step_num))

#先对总群组进行划分
get_group_list()

for i in range(0,len(client_list_group)):
    with client_list_group[i]:
        client_list_group[i].loop.run_until_complete(main(i))
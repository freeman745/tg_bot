from telethon import TelegramClient

#客户列表。需要手动添加
client_list = []
def getClient(api_id,api_hash,phone,*proxy): #*proxy为三元组 ，
    if len(proxy) != 3:
        client = TelegramClient('{phone}.session'.format(phone=phone),api_id=api_id,api_hash=api_hash)
    else:
        client = TelegramClient('{phone}.session'.format(phone=phone), api_id=api_id, api_hash=api_hash,proxy=proxy)
    try:
        client.start()
    except:
        client.start(password='w……')
    # print('client1 是否连接：', client.is_connected())
    if client.is_connected():
        print("+++用户【{}】+++".format(phone), '连接成功')
        return client
    else:
        print("---用户【{}】---".format(phone),'连接失败')
# client_list.append(client2)
#=================================================================
#  +8617344494726

api_id = 29633944
api_hash = 'ba2fdba75a616a9eb629f70cca0f5058'
phone = 818080841781
client_list.append(getClient(api_id,api_hash,phone,''))

#=================================================================

#=================================================================
#   +8615303517524
'''
phone = 639621645257
api_id = 28126027
api_hash = '9569a514df3e7be08970ba756ae14630'
client_list.append(getClient(api_id,api_hash,phone,''))
'''
#代理需要自行更换，防止多次登录，禁止号码
#client_list.append(getClient(api_id,api_hash,phone,socks.SOCKS5,'localhost','4444'))#socks.SOCKS5,'localhost','4444' 为proxy的三元组
#=================================================================



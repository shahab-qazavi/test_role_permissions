__author__ = 'Shahab Qazavi'

import sys
import os
sys.path.append(os.getcwd())
import requests
from public_role import consts


def init_database_without_user():
    data = {'secret': 'VeryStrong$ecret'}
    requests.get(consts.SERVER_ADDRESS + '/init_database_for_test', data=data)


def init_database():
    data = {'secret': 'VeryStrong$ecret'}
    result = requests.get(consts.SERVER_ADDRESS + '/init_database_for_test', data=data)
    consts.ADMIN_TOKEN = get_admin_token()['token']

    consts.USER1_INFO = create_user_by_admin(consts.ADMIN_TOKEN,'0919','qazav','22','shahab').json()
    consts.USER1_LOGIN = login('0919','22')
    consts.USER1_TOKEN = consts.USER1_LOGIN['token']
    consts.USER1_ID = consts.USER1_INFO['data']['item']['id']

    consts.USER2_INFO = create_user_by_admin(consts.ADMIN_TOKEN,'0939','qzav','23','mamad').json()
    consts.USER2_LOGIN = login('0939', '23')
    consts.USER2_TOKEN = consts.USER2_LOGIN['token']
    consts.USER2_ID = consts.USER2_INFO['data']['item']['id']

    consts.USER3_INFO = create_user_by_admin(consts.ADMIN_TOKEN,'0912','qazv','24','shahab').json()
    consts.USER3_LOGIN = login('0912', '24')
    consts.USER3_TOKEN = consts.USER3_LOGIN['token']
    consts.USER3_ID = consts.USER3_INFO['data']['item']['id']

    consts.SERVICE11_ID = add_service_by_user(consts.USER1_TOKEN, 'something11', '0916', 'some title111')['data']['item']['id']
    consts.SERVICE12_ID = add_service_by_user(consts.USER1_TOKEN, 'something12', '0917', 'some title112')['data']['item']['id']
    consts.SERVICE21_ID = add_service_by_user(consts.USER2_TOKEN, 'something21', '0918', 'some title221')['data']['item']['id']
    consts.SERVICE22_ID = add_service_by_user(consts.USER2_TOKEN, 'something22', '0919', 'some title222')['data']['item']['id']


def get_admin_token():
    data = {'code':'+98','mobile': 'admin', 'password': '1', 'locale': 'en'}
    result = requests.post(consts.SERVER_ADDRESS + '/login', json=data)
    output = result.json()
    return output


def get_complex_token():
    admin_token = get_admin_token()['token']
    data = {'token':admin_token,'code': '+98', 'mobile': 'complex', 'password': '1',
            'locale': 'en', 'family': 'com', 'role': 'complex'}
    requests.post(consts.SERVER_ADDRESS + '/users', json=data)
    data = {'mobile': 'complex','password': '1','code':'+98'}
    result = requests.post(consts.SERVER_ADDRESS + '/login', json=data)
    output = result.json()
    return output['token']


def get_user_token():
    admin_token = get_admin_token()['token']
    data = {'token':admin_token,'code': '+98', 'mobile': 'user', 'password': '1',
            'locale': 'en', 'family': 'us', 'role': 'user'}
    requests.post(consts.SERVER_ADDRESS + '/users', json=data)
    data = {'mobile': 'user','password': '1','code':'+98'}
    result = requests.post(consts.SERVER_ADDRESS + '/login', json=data)
    output = result.json()
    return output['token']


def get_operator_token():
    admin_token = get_admin_token()['token']
    data = {'token':admin_token,'code': '+98', 'mobile': 'operator', 'password': '1',
            'locale': 'en', 'family': 'op', 'role': 'operator'}
    requests.post(consts.SERVER_ADDRESS + '/users', json=data)
    data = {'mobile': 'operator','password': '1','code':'+98'}
    result = requests.post(consts.SERVER_ADDRESS + '/login', json=data)
    output = result.json()
    return output['token']


def get_reporter_token():
    admin_token = get_admin_token()['token']
    data = {'token':admin_token,'code': '+98', 'mobile': 'reporter', 'password': '1',
            'locale': 'en', 'family': 'rep', 'role': 'reporter'}
    requests.post(consts.SERVER_ADDRESS + '/users', json=data)
    data = {'mobile': 'reporter','password': '1','code':'+98'}
    result = requests.post(consts.SERVER_ADDRESS + '/login', json=data)
    output = result.json()
    return output['token']


def get_guest_token():
    data = {'mobile': 'guest','password': '1','code':'+98'}
    result = requests.post(consts.SERVER_ADDRESS + '/login', json=data)
    output = result.json()
    return output['token']


def create_user_by_admin(token, mobile, family, password,name):
    data = {'role':'user','code':'+98','mobile': mobile,'name':name,'family':family,'password':password,'token': token}
    result = requests.post(consts.SERVER_ADDRESS + '/users', json=data)
    return result


def register_user(mobile, family, password , name, referer=''):
    data = {'code':'+98','mobile': mobile,'family':family,'name':name,'password':password, 'referer': referer}
    result = requests.post(consts.SERVER_ADDRESS + '/register', json=data)

    return result


def login(mobile, password):
    data = {'code': '+98', 'mobile': mobile, 'password': password}
    result = requests.post(consts.SERVER_ADDRESS + '/login', json=data)
    output = result.json()
    return output


def add_service_by_user(user_token, description, phone, title):
    data = {'description': description, 'location': {'type': 'Point', 'coordinates': [51.43470727, 32.49170482]},
            'code': '+98', 'city_id': '', 'phone': phone, 'category_id': '', 'title': title,
            'token': user_token}
    result = requests.post(consts.SERVER_ADDRESS + '/services', json=data)
    output = result.json()
    return output


def get_service_by_user(user_token, object_service):
    data = {'token': user_token}
    result = requests.get(consts.SERVER_ADDRESS + object_service , data=data)
    output = result
    return output


def confirmed_by_admin(id_service, admin_token, object_service):
    data = {'id': id_service, 'confirmed': True, 'token': admin_token}
    result = requests.put(consts.SERVER_ADDRESS + object_service, json=data)
    return result.json()


def add_comment_by_user(user_token, service_id,comment):
    data = {'text': comment, 'service_id': service_id, 'token': user_token}
    result = requests.post(consts.SERVER_ADDRESS + '/services_comment', json=data)
    output = result.json()
    return output['data']['item']['id']


def send_message(token,message,user_name,user_id,conversation_id=''):
    data = {'token': token, 'message': message, 'user_name': user_name,
            'user_id': user_id,'conversation_id':conversation_id}
    result = requests.post(consts.SERVER_ADDRESS + '/chat', json=data)
    return result


def get_conversation(token,conversation_id=''):
    data = {'token': token,'conversation_id':conversation_id}
    result = requests.get(consts.SERVER_ADDRESS + '/my_conversations', data=data)
    return result


def create_10_service():
    a = 1
    create_user_by_admin(get_admin_token()['token'], '0933', 'qazavi', '23', 'shah hab')
    user_login= login('0939', '23')
    user_token= user_login['token']
    for x in range(0,10):
        add_service_by_user(user_token, 'something'+str(a), '091'+str(a), 'some title'+str(a))
        a += 1


def create_categories(name_categories,default):
    data={'token':consts.ADMIN_TOKEN,'name':name_categories,'type':'private','default':default,'parent_id':''}
    result=requests.post(consts.SERVER_ADDRESS+'/categories',json=data)
    return result

def add_tags(tag):
    data={'token':consts.ADMIN_TOKEN,'name':tag,'default':True}
    result=requests.post(consts.SERVER_ADDRESS+'/tags',json=data)
    return result


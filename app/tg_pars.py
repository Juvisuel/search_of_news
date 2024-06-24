import random
import time
from ctypes import *
import json
import sys
import pandas as pd
import datetime


# Сброс ограничений на количество выводимых рядов
from f import f_time

pd.set_option('display.max_rows', None)

# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)
pd.options.display.expand_frame_repr = False

## Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)

# tdjson_path = find_library("tdjson") or "tdjson.dll"
# if tdjson_path is None:
#     raise RuntimeError(
#         "TDLib is not found on the system. "
#         "Please, follow instructions at https://git.io/tdlib to install it."
#     )
tdjson_path = 'F:/learn_neuro/vc_analytics/tdLib_folder/td/build/Release/tdjson.dll'

with open('F:/learn_neuro/vc_analytics/tech_files\path', 'r') as temp:
    local_path = temp.read()

with open('F:/learn_neuro/vc_analytics/tech_files/api_hash', 'r') as temp:
    api_hash = temp.read()

tdjson = CDLL(tdjson_path)

# load TDLib functions from shared library
_td_create_client_id = tdjson.td_create_client_id
_td_create_client_id.restype = c_int
_td_create_client_id.argtypes = []

_td_receive = tdjson.td_receive
_td_receive.restype = c_char_p
_td_receive.argtypes = [c_double]

_td_send = tdjson.td_send
# _td_send.restype = None
_td_send.argtypes = [c_int, c_char_p]

_td_execute = tdjson.td_execute
_td_execute.restype = c_char_p
_td_execute.argtypes = [c_char_p]

log_message_callback_type = CFUNCTYPE(None, c_int, c_char_p)

_td_set_log_message_callback = tdjson.td_set_log_message_callback
_td_set_log_message_callback.restype = None
_td_set_log_message_callback.argtypes = [c_int, log_message_callback_type]

# initialize TDLib log with desired parameters
@log_message_callback_type
def on_log_message_callback(verbosity_level, message):
    if verbosity_level == 0:
        sys.exit('TDLib fatal error: %r' % message)

def td_execute(query):
    query = json.dumps(query).encode('utf-8')
    result = _td_execute(query)
    if result:
        result = json.loads(result.decode('utf-8'))
    return result

_td_set_log_message_callback(2, on_log_message_callback)

# setting TDLib log verbosity level to 1 (errors)
td_execute({'@type': 'setLogVerbosityLevel', 'new_verbosity_level': 1, '@extra': 1.01234})

# create client
client_id = _td_create_client_id()

# simple wrappers for client usage
def td_send(query):
    query = json.dumps(query).encode('utf-8')
    _td_send(client_id, query)

def td_receive():
    result = _td_receive(1.0)
    if result:
        result = json.loads(result.decode('utf-8'))
    return result

def test_send_receve(temp_name=1.):

    result = {}
    result_check = 0

    while result_check < 1:
    # while True:

        # time.sleep(0.1)
        # main events
        event = td_receive()

        try:

            if '@extra' in event:
                # print(str(event))
                result = event
                result_check += 1
                # process authorization states
                if event['@type'] == 'updateAuthorizationState':
                    auth_state = event['authorization_state']

                    # # if client is closed, we need to destroy it and create new client
                    if auth_state['@type'] == 'authorizationStateClosed':
                        print('need close')


                    # set TDLib parameters
                    # you MUST obtain your own api_id and api_hash at https://my.telegram.org
                    # and use them in the setTdlibParameters call
                    if auth_state['@type'] == 'authorizationStateWaitTdlibParameters':
                        td_send({'@type': 'setTdlibParameters',
                                 'database_directory': 'tdlib',
                                 'use_message_database': True,
                                 'use_secret_chats': True,
                                 'api_id': 29867020,
                                 'api_hash': api_hash,
                                 'system_language_code': 'en',
                                 'device_model': 'Desktop',
                                 'application_version': '1.0',
                                 'enable_storage_optimizer': True})

                    # enter phone number to log in
                    if auth_state['@type'] == 'authorizationStateWaitPhoneNumber':
                        phone_number = input('Please enter your phone number: ')
                        td_send({'@type': 'setAuthenticationPhoneNumber', 'phone_number': phone_number})

                    # enter email address to log in
                    if auth_state['@type'] == 'authorizationStateWaitEmailAddress':
                        email_address = input('Please enter your email address: ')
                        td_send({'@type': 'setAuthenticationEmailAddress', 'email_address': email_address})

                    # wait for email authorization code
                    if auth_state['@type'] == 'authorizationStateWaitEmailCode':
                        code = input('Please enter the email authentication code you received: ')
                        td_send({'@type': 'checkAuthenticationEmailCode',
                                 'code': {'@type': 'emailAddressAuthenticationCode', 'code': code}})

                    # wait for authorization code
                    if auth_state['@type'] == 'authorizationStateWaitCode':
                        code = input('Please enter the authentication code you received: ')
                        td_send({'@type': 'checkAuthenticationCode', 'code': code})

                    # wait for first and last name for new users
                    if auth_state['@type'] == 'authorizationStateWaitRegistration':
                        first_name = input('Please enter your first name: ')
                        last_name = input('Please enter your last name: ')
                        td_send({'@type': 'registerUser', 'first_name': first_name, 'last_name': last_name})

                    # wait for password if present
                    if auth_state['@type'] == 'authorizationStateWaitPassword':
                        password = input('Please enter your password: ')
                        td_send({'@type': 'checkAuthenticationPassword', 'password': password})

                sys.stdout.flush()
        except:
            pass

    return result

tdlib_params = {'@type': 'setTdlibParameters',
                         'database_directory': 'tdlib',
                         'use_message_database': True,
                         'use_secret_chats': True,
                         'api_id': 29867020,
                         'api_hash': api_hash,
                         'system_language_code': 'en',
                         'device_model': 'Desktop',
                         'application_version': '1.0',
                         'enable_storage_optimizer': True,


                    }


def send_receve_custom_request(params, tdlib_params=tdlib_params):
    temp_name = datetime.datetime.now().timestamp()
    params['@extra'] = temp_name
    td_send(tdlib_params)
    td_send(params)
    result = test_send_receve(temp_name=temp_name)

    return result


def get_name_from_id(id):


    params = {
        "@type": "getUser",
        "user_id": str(id)

    }

    result = send_receve_custom_request(params)

    return result


def get_id_channel(group_name):

    # найти ID по имени
    # group_name = 'vaverka888'

    # получение ID по имени
    params = {
        "@type": "searchPublicChat",
        "username": group_name,
    }

    print(params)

    #
    # # получение имени по ID  ##### https://core.telegram.org/tdlib/docs/classtd_1_1td__api_1_1_function.html
    # params = {
    #     "@type": "getUser",
    #     "user_id": '1852660010'
    #
    # }


    ### получение ID по имени
    result = send_receve_custom_request(params)
    # print(result)
    chat_id = result['id']

    from_message_id = 0

    return chat_id

#
# # нулевое сообщение
# params = {'@type': "getChatHistory",
#           'chat_id': chat_id,
#           'limit': 100,
#           'from_message_id': from_message_id,
#           }
#
#
# #

def parse_message(message):


    out_list = []
    out_list.append(message['id'])
    out_list.append(message['date'])
    out_list.append(0)
    out_list.append(sum(x['total_count'] for x in (message['interaction_info']['reactions'])))
    out_list.append(message['interaction_info']['forward_count'])
    try:
        out_list.append(message['interaction_info']['reply_info']['reply_count'])
    except:
        out_list.append(0)
    print(message)
    out_list.append(message['interaction_info']['view_count'])

    try:
        print(message['content']['caption']['text'])
        out_list.append(message['content']['caption']['text'])
    except:
        try:
            print(message['content']['text']['text'])
            out_list.append(message['content']['text']['text'])
        except:
            out_list[2] = 'photo'
            out_list.append('')

    return out_list, message['id']


def parse_message_to_dict(message):
    out_dict = {}
    out_dict['public'] = message['id']
    out_dict['timestamp'] = message['date']

    try:
        out_dict['reactions'] = sum(x['total_count'] for x in (message['interaction_info']['reactions']))
    except:
        out_dict['reactions'] = 0

    try:
        out_dict['shares'] = message['interaction_info']['forward_count']
    except:
        out_dict['shares'] = 0

    try:
        out_dict['comments'] = message['interaction_info']['reply_info']['reply_count']
    except:
        out_dict['comments'] = 0

    try:
        out_dict['views'] = message['interaction_info']['view_count']
    except:
        out_dict['views'] = 0

    try:

        out_dict['text'] = message['content']['caption']['text']
    except:
        try:
            out_dict['text'] = message['content']['text']['text']

        except:
            out_dict['type'] = 'photo'
            out_dict['text'] = ''

    return out_dict, message['id']


def parse_deleted(message):
    print('deleted')

    out_dict = {}
    out_dict['public'] = message['id']
    out_dict['timestamp'] = message['date']

    try:
        out_dict['reactions'] = sum(x['total_count'] for x in (message['interaction_info']['reactions']))
    except:
        out_dict['reactions'] = 0

    try:
        out_dict['shares'] = message['interaction_info']['forward_count']
    except:
        out_dict['shares'] = 0

    try:
        out_dict['comments'] = message['interaction_info']['reply_info']['reply_count']
    except:
         out_dict['comments'] = 0

    try:
        out_dict['views'] = message['interaction_info']['view_count']
    except:
         out_dict['views'] = 0


    try:
        out_dict['text'] = message['content']['text']
    except:

        try:
            out_dict['text'] = message['content']['text']['text']

        except:
            out_dict['type'] = 'photo'


    return out_dict, message['id']


def parse_chat_message(message):
    print(message)
    out_list = []
    out_list.append(message['id'])
    out_list.append(message['date'])
    out_list.append(0)
    out_list.append(sum(x['total_count'] for x in (message['interaction_info']['reactions'])))
    out_list.append(message['interaction_info']['forward_count'])
    try:
        out_list.append(message['interaction_info']['reply_info']['reply_count'])
    except:
        out_list.append(0)
    print(message)
    out_list.append(message['interaction_info']['view_count'])

    try:
        print(message['content']['caption']['text'])
        out_list.append(message['content']['caption']['text'])
    except:
        out_list[2] = 'photo'
        out_list.append('')

    return out_list, message['id']


def parse_message_photo(message):

    out_list = []
    out_list.append(message['photo']['id'])
    out_list.append(message['date'])
    out_list.append(0)
    out_list.append(sum(x['total_count'] for x in (message['interaction_info']['reactions'])))
    out_list.append(message['interaction_info']['forward_count'])
    try:
        out_list.append(message['interaction_info']['reply_info']['reply_count'])
    except:
        out_list.append(0)
    print(message)
    out_list.append(message['interaction_info']['view_count'])

    try:
        out_list.append(message['content']['text']['text'])
    except:
        out_list[2] = 'photo'
        try:
            print(112121)
            print(message['content'] )
            out_list.append(message['content']['caption']['text'])
        except:
            out_list.append('')

    return out_list, message['id']


def join_channel(chat_id):
    params = {'@type': "joinChat",
              'chat_id': chat_id,
              }
    send_receve_custom_request(params)
    print('joined')

def leave_channel(chat_id):
    params = {'@type': "leaveChat",
              'chat_id': chat_id,
              }
    send_receve_custom_request(params)

    print('leaved')

def render_derivative(messages):
    derivative_table = pd.DataFrame(columns=['views', 'datetime', 'dev', 'date_dev','koof', 'mean_v'])

    for message in messages:

        datetime = message['date']

        try:
            views = message['interaction_info']['view_count']
        except:
            views = 0

        if derivative_table.shape[0] > 0:
            dev = views - derivative_table.loc[derivative_table.shape[0]-1, 'views']

            date_dev = derivative_table.loc[derivative_table.shape[0]-1, 'datetime'] - datetime

        else:
            dev = 0
            date_dev = 0


        derivative_table.loc[derivative_table.shape[0]] = [views, datetime, dev, date_dev, 0, 0]

    last_v = derivative_table.loc[derivative_table.shape[0]-1, 'views']
    first_v = derivative_table.loc[0, 'views']
    last_t = derivative_table.loc[derivative_table.shape[0]-1, 'datetime']
    first_t = derivative_table.loc[0, 'datetime']
    koof = (last_v-first_v)/(last_t-first_t)

    for i in derivative_table.index[:-1]:
        derivative_table.loc[i, 'koof'] = round(last_v - koof * (last_t - derivative_table.loc[i, 'datetime']))

    if derivative_table.shape[0] < 2:
        return derivative_table['mean_v'].tolist()

    derivative_table.loc[derivative_table.shape[0]-1, 'koof'] = round(koof * (last_t-first_t))

    derivative_table['mean_v'] = derivative_table['views'] / derivative_table['koof']

    return derivative_table['mean_v'].tolist()



#### рабочий скрипт парсинга Телеги
def create_bd_channel(chat_id, channel_name, item_name, days_ago=365):

    # создание бд
    columns = ['public', 'date', 'timestamp', 'attachments', 'likes', 'shares', 'comments', 'views', 'text', 'link',
               'geo', 'report',
               'request', 'all_score', 'base_match', 'zero_match', 'base_perc', 'zero_perc', 'ess_perc', 'dis_perc',
               'res_dir', 'res_dis', 'exciles']

    post_table = pd.DataFrame(columns=columns)
    last_post = 0
    params = {'@type': "getChatHistory",
              'chat_id': chat_id,
              'limit': 10,
              'from_message_id': 0,
              }


    def get_good_table():

        result_zero = send_receve_custom_request(params)
        print()
        # print('1 len', len(result_zero['messages']))
        date = result_zero['messages'][0]['date']
        # print(date)
        # print('date', datetime.datetime.fromtimestamp(result_zero['messages'][0]['date']).date())
        from_message_id = result_zero['messages'][0]['id']
        # print('from_message_id', from_message_id)


        from_message_id = result_zero['messages'][0]['id']
        # print('from_message_id', from_message_id)
        print()

        # # #
        # # #
        params['from_message_id'] = from_message_id
        # params['offcet'] = 0
        params['limit'] = 50
        time.sleep(random.random()*3)
        result = send_receve_custom_request(params)
        # print('2 len', len(result['messages']))
        result['messages'].insert(0, result_zero['messages'][0])

        derivative_list = render_derivative(result['messages'])

        for i, item in enumerate(result['messages']):
            # print()
            # print('item', item)

            date = item['date']
            # print(date)
            # проверка на дату

            if not f_time.in_some_hours(date, hours=days_ago*24):  # 31536000
                # проверка на дату

                # print('over date', datetime.datetime.fromtimestamp(date).date())

                # post_table.to_csv(f'F:/learn_neuro/data_vk/{local_path[1:-1]}/{local_path[1:-1]}.csv')
                return post_table
                # pass

            else:

                try:
                    res_dict, from_message_id = parse_message_to_dict(item)
                    print('some_finded')
                    print(res_dict)
                    # post_table.loc[post_table.shape[0]] = list_results

                except:

                    # try:
                    res_dict, from_message_id = parse_deleted(item)
                    print('okk')
                    # print(list_results)
                    # print(from_message_id)
                    print()
                    # post_table.loc[post_table.shape[0]] = list_results

                    # except:
                    ### проблема - на фотках нет лайков
                    # try:
                    #     x = item['photo']['caption']['text']
                    #     list_results, from_message_id = parse_message_photo(item)
                    #     list_results = [item['id'], item['date'], 0,0,0,0,0,'непонятное']
                    #     # post_table.loc[post_table.shape[0]] = list_results
                    #     print('no')
                if len(res_dict['text']) > 0:
                    post_table.loc[post_table.shape[0]] = 0
                    res_dict['date'] = datetime.datetime.fromtimestamp(date).date()
                    res_dict['request'] = item_name
                    res_dict['link'] = f'https://t.me/{channel_name}'
                    res_dict['exciles'] = int(derivative_list[i]*10)
                    for key in res_dict.keys():
                        post_table.loc[post_table.shape[0]-1, key] = res_dict[key]

    post_table = get_good_table()
    if post_table.shape[0] == 0:
        time.sleep(10)
        post_table = get_good_table()

    return post_table


def create_bd_chat(chat_id):
    params = {'@type': "getChatHistory",
              'chat_id': chat_id,
              'limit': 100,
              'from_message_id': 0,
              }

    # создание бд
    post_table = pd.DataFrame(columns=['id', 'date', 'attachments', 'likes', 'shares', 'comments', 'views', 'text'])
    result = send_receve_custom_request(params)

    list_results, from_message_id = parse_chat_message(result['messages'][0])

    while post_table.shape[0] < 1000:
        print()
        result = send_receve_custom_request(params)
        # print(result)

        # if result[]
        for item in result['messages']:
            print(item)



            try:
                x = item['content']['text']['text']
                list_results, from_message_id = parse_message(item)
                post_table.loc[post_table.shape[0]] = list_results

            except:
                try:
                    list_results, from_message_id = parse_deleted(item)

                    print('okk')
                    print(list_results)
                    print(from_message_id)
                    print()
                    post_table.loc[post_table.shape[0]] = list_results
                    print(post_table.loc[post_table.shape[0]-1])
                except:
                    ### проблема - на фотках нет лайков
                    # try:
                    #     x = item['photo']['caption']['text']
                    #     list_results, from_message_id = parse_message_photo(item)
                    list_results = [item['id'], item['date'], 0, 0, 0, 0, 0, 'непонятное']
                    post_table.loc[post_table.shape[0]] = list_results
                    print('no')
                pass

        ids = [x for x in post_table['id']]
        print(ids)
        print(from_message_id)
        count_cycles = len([x for x in ids if x == from_message_id])
        print(count_cycles)
        if count_cycles > 1:
            break
        elif result['total_count'] < 10 and len(ids) > 2:
            break
        else:
            params = {'@type': "getChatHistory",
                      'chat_id': chat_id,
                      'limit': 100,
                      'from_message_id': from_message_id,
                      }

        print('post_table')
        print(post_table)

    post_table = post_table.drop(0, axis=0)
    return post_table


def get_public_and_return_base_table_last_day(channel_name, item_name, days_ago=1):
    print()
    channel_id = get_id_channel(channel_name)
    time.sleep(random.random()*5)
    join_channel(channel_id)
    time.sleep(random.random()*3)
    post_table = create_bd_channel(channel_id, channel_name, item_name, days_ago=days_ago)
    time.sleep(random.random()*3)
    leave_channel(channel_id)
    print(post_table)
    return post_table

def joined(channel_name):
    channel_id = get_id_channel(channel_name)
    time.sleep(3)
    join_channel(channel_id)
    leave_channel(channel_id)



# post_table = get_public_and_return_base_table_last_day('Nuihorsnym', 'Катюша', days_ago=2)
# print(post_table)


# post_table = create_bd_channel(params, days_ago=60)
# post_table = create_bd_chat(params)
#
# post_table.to_csv(f'F:/learn_neuro/data_vk/{local_path[1:-1]}/{local_path[1:-1]}.csv')



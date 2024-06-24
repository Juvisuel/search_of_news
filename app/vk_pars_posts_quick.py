from datetime import datetime, timedelta
import requests
import time
import pandas as pd
from news_search_f import f_time, f_text_encode, f_geo

pd.set_option('display.max_colwidth', 100)

def time_check(text):  ### для ускорения нужна нейронка тут
    text = f_text_encode.encode_text_without_normalize(text)
    futr, past, pres = 0, 0, 0

    for word in text:
        try:
            [past_0, pres_0, futr_0] = f_text_encode.is_time(word)
            past += past_0
            futr += futr_0
            pres += pres_0
        except:
            pass
    list_times = [past, pres, futr]

    if sum(list_times) > 0:
        max_list_times = max(list_times)
        list_times = [x / max_list_times for x in list_times]

    return list_times


def rec_check(text, list_no_words=['акция', 'курс', 'заказ', 'закаж', 'закупка', 'приглаша', 'можете обратиться', 'открыта запись',
                                   'звоните', 'бесплатн','оплат', 'стоимость', 'подписывайтесь',  'расписани', 'марафон',  'розыгрыш', 'все включено', 'билет']):
    for word in list_no_words:
        if word in text:
            return False
    return True


def get_public_and_return_base_table_last_day(id_us, group_n, days_ago=1, max_len_text=500):

    main_url = 'https://api.vk.com/method/'
    tech_str_1 = 'wall.getById?posts='

    with open('F:/learn_neuro/vc_analytics/tech_files/tok2', 'r') as temp:
        tok = temp.read()

    with open('F:/learn_neuro/vc_analytics/tech_files/path', 'r') as temp:
        local_path = temp.read()


    # id_us = '-212697586'
    # n_post = '1'

    # это для группы
    # group_n = '-212697586'
    param = {'access_token': tok,  'user_id': id_us, 'v': 5.131}
    method2 = 'wall.get?posts='
    geo = 0

    # на сколько постов назад делаем и первый пост

    # last_post = 1625   #номер последнего поста
    # days_ago = 365  # насколько назад
    # begin_post = last_post-2000  #номер поста

    # # # это для пользователя
    #
    # group_n = '553948034'
    # param = {'access_token': tok, 'owner_id':id_us, 'v':5.131  }
    # method2 = 'wall.get?posts='


    # todo написать добор постов, которые пришли с момента прежней интерпретации

    try:
        post_table_old = pd.read_csv(f'F:/learn_neuro/data_vk/{local_path[1:-1]}/{local_path[1:-1]}.csv')
        post_table_old = post_table_old.drop('Unnamed: 0', axis=1)
        exist = 1
        base_date = int(post_table_old.loc[0, 'date'])

    except:
        exist = 0
        base_date = 0
        post_table_old = pd.DataFrame(columns=['public', 'date', 'timestamp', 'attachments', 'likes', 'shares', 'comments', 'views', 'text', 'link', 'geo'])


    post_table = pd.DataFrame(columns=['public', 'date',  'timestamp', 'attachments', 'likes', 'shares', 'comments', 'views', 'text', 'geo'])

    print('exist', exist, base_date)

    # новый парс
    date = datetime.datetime.now().timestamp()  #todo переписать на таймштамп текущей даты, и сразу задать границу в год и прописать ее внизу на чеке даты
    # id_post = last_post
    offcet = 1
    break_marker = 0


    time.sleep(3)


    delta = 1
    param = {'access_token': tok, 'owner_id': id_us, 'offset': offcet, 'count': delta, 'v': 5.131}
    request_url = f'{main_url}{method2}{group_n}'
    # request_url = f'{main_url}{method2}{group_n}_{id_post}'
    rec = requests.get(url=request_url, params=param)
    # print(rec)
    rec_json_full = rec.json()
    # print(len(rec_json_full))
    # print('rec_json_full_f', rec_json_full_f)
#     rec = requests.get(url=f'{main_url}{method2}{group_n}{str(id_post)}', params=param)
#     rec_json_full = rec.json()

    for i, rec_json in enumerate(rec_json_full['response']['items']):
        print(i)
    # for rec_json in rec_json_full['response'] :

        # print('rec_json', rec_json)



        try:
            h = rec_json['is_deleted']
            pass

        except:

            if rec_json['marked_as_ads']:
                print('реклама')
                break

            try:
                date = rec_json['date']
                # проверка на дату
                # print('days_ago', days_ago)
                if not f_time.in_some_days(date, days=days_ago):  # 31536000
                    # проверка на дату
                    print('over date', datetime.datetime.fromtimestamp(date).date())
                    break_marker = 1
                    # post_table.to_csv(f'F:/learn_neuro/data_vk/{local_path[1:-1]}/{local_path[1:-1]}.csv')
                    return post_table

                ## проверка на геолокацию
                date = datetime.datetime.fromtimestamp(date)
                try:
                    attachments = rec_json['attachments']['type']
                except:
                    try:
                        attachments = rec_json['attachments'][0]['type']
                    except:
                        attachments = ''
                likes = rec_json['likes']['count']
                shares = rec_json['reposts']['count']
                text = rec_json['text']

                views = rec_json['views']['count']


                try:
                    comments = rec_json['comments']['count']
                except:
                    comments = 0

                if len(text) > 120 and len(text.split()) < max_len_text:
                    post_number = rec_json['id']
                    link = f'https://vk.com/wall{id_us}_{post_number}'
                    post_table.loc[post_table.shape[0]] = [id_us, date, attachments, likes, shares,  comments, views, text, link, geo]

                # try:
                #     url_bag = rec_json['attachments'][0]['photo']['sizes']
                #     last_index = len(url_bag)-1
                #     picture_url = url_bag[last_index]['url']
                #     # pict = requests.get(picture_url).content
                #     # with open(f'F:/learn_neuro/data_vk/{local_path[1:-1]}/pictures/{temp_id_post}.jpg', 'wb') as handler:
                #     #     handler.write(pict)
                # except:
                #     print('no')
                #     pass

            except:
                print('dont2')
                pass



    #
    return post_table
    #
    # # проверка на последний блок
    # offcet = offcet + delta
    # if offcet < 0 or delta == 0:
    #     print(post_table)
    #     print('over offcet')
    #     # post_table.to_csv(f'F:/learn_neuro/data_vk/{local_path[1:-1]}/{local_path[1:-1]}.csv')
    #     return post_table
    #     # break


## внутренний цикл
def inner_cycle(rec_json_full, post_table, i, input_dict, list_no_words, back_drive, max_len_text, geo, question, time_bounded, question_hard ):

    # searched_hard = f_text_encode.get_phrase_and_return_all_forms(input_dict['question_hard'][i])
    # if len(searched_hard) == 0:
    #     searched_hard = [input_dict['question_hard'][i]]

    ## нам пришло какое то количество записей от реквеста, мы их пошли перебирать по одной
    for y, rec_json in enumerate(rec_json_full['response']['items']):
        # print(question)
        # print(rec_json)
        try:
            h = rec_json['is_deleted']
            pass

        except:

            try:
                date = rec_json['date']

                # проверка на дату
                # if not f_time.in_some_days(date, days=back_drive):  # 31536000
                #     print('over date')
                #     return post_table, 5

                ## если была задана геолокация, то мы берем только тегнутые по месту новости
                timestamp = date
                date = datetime.fromtimestamp(date)

                ## эти данные в реквесте не всегда, берем если есть
                try:
                    attachments = rec_json['attachments']['type']

                except:
                    try:
                        attachments = rec_json['attachments'][0]['type']
                    except:
                        attachments = ''
                try:
                    likes = rec_json['likes']['count']

                except:
                    likes = 0
                try:
                    shares = rec_json['reposts']['count']

                except:
                    shares = 0
                text = rec_json['text']

                ## проверяем вхождение жесткого ключевика
                if question_hard in text:
                    print('in')
                    ## проверяем что такого текста нет
                    if text[:50] not in ' '.join(list(post_table['text'])):
                        # print(text[:50] , question)

                        ## дефолтный чек на рекламу
                        if rec_check(text.lower()):
                            # print('not adv')
                            ## чек на нежелательные слова
                            if rec_check(text.lower(), list_no_words=list_no_words):
                                # print('loc_ words')

                                id_us = rec_json['owner_id']
                                # print(rec_json['id'])

                                try:
                                    comments = rec_json['comments']['count']
                                    views = rec_json['views']['count']
                                except:
                                    comments = 0
                                    views = 0

                                ## проверка на длину текста
                                if len(text.split()) < max_len_text:
                                    # print('len ok')

                                        if time_bounded[0] == 'on':
                                            list_times = time_check(text)
                                            # print(text[:200])
                                            # print(list_times)
                                            if 'past' in time_bounded[1]:

                                                if list_times[0] > list_times[1] and list_times[0] > list_times[2]:
                                                    # print('ok time past')

                                                    post_number = rec_json['id']

                                                    link = f'https://vk.com/wall{id_us}_{post_number}'
                                                    print('to table 1 ')

                                                    post_table.loc[post_table.shape[0]] = [id_us, date, timestamp,
                                                                                           attachments,
                                                                                           likes,
                                                                                           shares,
                                                                                           comments,
                                                                                           views, text[:2000], link,
                                                                                           geo,
                                                                                           question]


                                                    # print('itsok' )

                                                else:
                                                    pass
                                                    # print('no ok time past')

                                            if 'pres' in time_bounded[1]:
                                                if list_times[0] < list_times[1] and list_times[1] > list_times[2]:
                                                    # print('ok time pres')

                                                    post_number = rec_json['id']

                                                    link = f'https://vk.com/wall{id_us}_{post_number}'
                                                    print('to table 1 ')

                                                    post_table.loc[post_table.shape[0]] = [id_us, date, timestamp,
                                                                                           attachments,
                                                                                           likes,
                                                                                           shares,
                                                                                           comments,
                                                                                           views, text[:2000], link,
                                                                                           geo,
                                                                                           question]


                                                    # print('itsok')

                                                else:
                                                    pass
                                                    # print('no ok time pres')

                                        else:
                                            # print('no time bound')
                                            post_number = rec_json['id']

                                            link = f'https://vk.com/wall{id_us}_{post_number}'
                                            print('to table 1 ')

                                            post_table.loc[post_table.shape[0]] = [id_us, date, timestamp,
                                                                                   attachments,
                                                                                   likes,
                                                                                   shares,
                                                                                   comments,
                                                                                   views, text[:2000], link,
                                                                                   geo,
                                                                                   question]


                                            # print('itsok')

                                else:
                                    pass
                                    # print('gigant', len(text.split()))

                        else:
                            pass
                            # print('adv')

                else:

                    pass

                    # print('gigant')

                ### картинки
                # try:
                #     url_bag = rec_json['attachments'][0]['photo']['sizes']
                #     last_index = len(url_bag)-1
                #     picture_url = url_bag[last_index]['url']
                #     pict = requests.get(picture_url).content
                #     # with open(f'F:/learn_neuro/data_vk/{local_path[1:-1]}/pictures/{temp_id_post}.jpg', 'wb') as handler:
                #     #     handler.write(pict)
                # except:
                #     print('no')
                #     pass

            except:
                pass


    return post_table

## основной скрипт поиска
def get_news_feed_last_day(input_dict, list_questions):

    # забираем кастомные настройки для парсинга
    ## максимальная длина текста
    max_len_text = input_dict['max_len_text']
    latitude = input_dict['latitude']
    longitude = input_dict['longitude']
    ## нежелательные слова
    list_no_words = input_dict['list_no_words']
    ## количество в запросе
    count = input_dict['count']
    ## ограничено по времени
    time_bounded = input_dict['time_bounded']
    ## сколько времени назад
    back_drive = input_dict['back_drive']
    ## делать ли склонение ключевиков
    mode_change = input_dict['mode_change']
    ## сколько постов ищем (количество ключевиков на эту переменную)
    nevod = input_dict['nevod']
    mode_time = input_dict['mode_time']
    over_end_time = int(datetime.now().timestamp())
    ## точные вхождения запросов
    question_hard_list = input_dict['question_hard'] if len(input_dict['question_hard']) > 0 \
                                                        else [x[0] for x in list_questions]

    ## модификация времени поиска - какое то время назад в днях
    if mode_time == 'back_drive':
        start_time = datetime.now()
        back_drive =timedelta(days=back_drive)
        delta = timedelta(days=1)
        start_time = start_time-back_drive
        end_time = start_time + delta

        start_time = int(datetime.timestamp(start_time))
        end_time = int(datetime.timestamp(end_time))
        print('start_time', start_time, 'back_drive', back_drive, 'start_time', start_time)

    ## модификация времени поиска - определенные даты определенных лет
    elif mode_time == 'some_time':
        some_time_dict = input_dict['some_time']
        some_time_dict_vith_vars = {}
        for key in some_time_dict.keys():
            if some_time_dict[key] != 'some':
                some_time_dict_vith_vars[key] = [some_time_dict[key]]
            else:
                if key == 'y':
                    some_time_dict_vith_vars[key] = [x for x in range(2021, 2024)]
                elif key == 'm':
                    some_time_dict_vith_vars[key] = [x for x in range(1, 13)]
                elif key == 'd':
                    some_time_dict_vith_vars[key] = [x for x in range(1, 31)]

        out_dates_list = []
        for year in some_time_dict_vith_vars['y']:
            for month in some_time_dict_vith_vars['m']:
                for day in some_time_dict_vith_vars['d']:
                    date_day = datetime(int(year), int(month), int(day))
                    out_dates_list.append(date_day)

        delta = timedelta(days=1)
        start_time = out_dates_list.pop(0)
        end_time = start_time + delta
        start_time = int(datetime.timestamp(start_time))
        end_time = int(datetime.timestamp(end_time))

    ## общие для методов апи
    main_url = 'https://api.vk.com/method/'
    tech_str_1 = 'wall.getById?posts='

    with open('F:/learn_neuro/vc_analytics/tech_files/tok2', 'r') as temp:
        tok = temp.read()

    method2 = 'newsfeed.search'

    # todo написать добор постов, которые пришли с момента прежней интерпретации
    # итоговая таблица
    post_table = pd.DataFrame(columns=['public', 'date', 'timestamp', 'attachments', 'likes', 'shares',
                                       'comments', 'views', 'text', 'link', 'geo', 'request'])

    print(question_hard_list)
    ## для каждого ключевика
    for i, [question1, geo] in enumerate(list_questions):
        print(13131, question1, question_hard_list[i])
        if mode_change == 'on':  ## склонение
            question_form_list = f_text_encode.get_phrase_and_return_all_forms(question1)
            if question_hard_list[i] == question1:
                question_hard_list_temp = question_form_list.copy()
            else:
                question_hard_list_temp = f_text_encode.get_phrase_and_return_all_forms(question_hard_list[i])

            if len(question_form_list) == 0:
                question_form_list = [question1]
                question_hard_list_temp = [question1]
            else:
                question_form_list.insert(0, question1)
                question_hard_list_temp.insert(0, question1)
        else:
            question_form_list = [question1]
            question_hard_list_temp = [question_hard_list[i]]

        for y, question in enumerate(question_form_list):
            try:
                question_hard = question_hard_list_temp[y]
            except:
                question_hard = question_hard_list_temp[0]
            print(question, question_hard)

            # новый парс

            if latitude == 0 and longitude == 0:
                param = {'q': f"{question}", 'access_token': tok, 'count': count, 'v': 5.131, 'start_time': start_time, 'end_time': end_time}
            else:
                param = {'q': f"{question}", 'access_token': tok, 'count': count, 'v': 5.131, 'latitude': latitude,
                         'longitude': longitude, 'start_time': start_time, 'end_time': end_time}


            time.sleep(1)

            cycle = 0

            while post_table.shape[0] < nevod or cycle == 0:
                time.sleep(1)
                print(post_table.shape[0], nevod, cycle)


                request_url = f'{main_url}{method2}'
                rec = requests.get(url=request_url, params=param)
                # print(rec)

                rec_json_full = rec.json()
                # print(rec_json_full)
                # count_seen += len(rec_json_full['response']['items'])


                try:
                    # print('получено', len(rec_json_full['response']['items']))
                    # print('след', rec_json_full['response']['next_from'])

                    ## пробуем сделать перебор
                    param['start_from'] = rec_json_full['response']['next_from']

                except:
                    ## меняем дату поиска на новую
                    if mode_time == 'back_drive':
                        try:
                            if start_time < post_table.loc[post_table.shape[0]-1, 'timestamp']:
                                start_time_temp = datetime.datetime.fromtimestamp(post_table.loc[post_table.shape[0]-1, 'timestamp'])
                            else:
                                start_time_temp = datetime.datetime.fromtimestamp(start_time) + delta
                            end_time = start_time_temp + delta
                            start_time = int(datetime.datetime.timestamp(start_time_temp))
                            param['start_time'] = start_time
                            param['end_time'] = int(datetime.datetime.timestamp(end_time))
                            print('try with no start from')
                        except:

                            print('no more')
                            break

                    elif mode_time == 'some_time':
                        try:
                            start_time = out_dates_list.pop(0)
                            end_time = start_time + delta
                            start_time = datetime.timestamp(start_time)
                            param['start_time'] = start_time
                            param['end_time'] = int(datetime.timestamp(end_time))
                        except:

                            print('no more')
                            break


                if cycle == 0:
                    ## результат парсинга уходит на отсев
                    post_table = inner_cycle(rec_json_full, post_table, i, input_dict, list_no_words,
                                             back_drive, max_len_text, geo, question, time_bounded, question_hard)

                if post_table.shape[0] >= nevod * len(list_questions):
                    cycle += 1
                    print('cycle', cycle, nevod)
                    # return post_table

                if start_time > over_end_time:
                    print('over_time')
                    return post_table

    return post_table
    #
    # # проверка на последний блок
    # offcet = offcet + delta
    # if offcet < 0 or delta == 0:
    #     print(post_table)
    #     print('over offcet')
    #     # post_table.to_csv(f'F:/learn_neuro/data_vk/{local_path[1:-1]}/{local_path[1:-1]}.csv')
    #     return post_table
    #     # break


# post_table = get_news_feed_last_day('зубы кошка люди боль', days_ago=1 )


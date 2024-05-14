import datetime
import re
import time
import local_check_post   ### todo заменить на api val
import pandas as pd
from app import vk_pars_posts_quick

list_no_words = ['предлага', 'приглаша', 'можете обратиться', 'звоните', 'бесплатн','оплат', 'стоимост', 'подписывайтесь', 'цен', 'расписани', 'марафон', 'руб.', 'все включено']
# list_no_words = []
# for item in list_no_words:
# 	list_no_words.extend(get_phrase_and_return_all_forms(list_no_words1))


smail = pd.read_csv('F:/learn_neuro/emo_bot/docs/smails.csv')
smail = ''.join(list(smail['smail']))


ymcaprimecenter_dict = {'local_path': 'ymcaprimecenter_vk',
				 'list_question': [['языковая школа барнаул', 'off'],['англий‌скии ‌барнаул', 'off'], ['изучение англий‌ского барнаул', 'off'], ['языки онлайн', 'off'],
								   ['языковая школа онлайн', 'off'],['Иностранные языки барнаул', 'off'],['китайский язык', 'off'],['китайский онлайн', 'off'],
									['барнаул 22 языки', 'off'],['Изучение языков онлайн', 'off'],['бюро переводов', 'off'],['нотариально заверенный перевод', 'off'],
								   ['Перевод с языка', 'off'],['Традиции Англии', 'off'], ['Традиции Китая', 'off']],

				'question_hard': ['языковая школа', '', 'изучение англий‌ского', 'языки', 'языковая школа', 'Иностранные языки', 'китайский язык',
								 'китайский', 'барнаул 22', 'Изучение языков', 'бюро переводов', 'нотариально заверенный', 'Перевод', 'Традиции', 'Традиции'],
				'max_len_text': 1000,
				'latitude': 0,
				'longitude': 0,
				'list_of_ids': [],
						'cenze': 75,
						'theme_cenze': 140,
						'all_score_cenze': 60,
						'mode':'expert',
			  	'count':20,
				 'list_no_words':list_no_words,
						'time_bounded': ['off']
,
				'back_drive': 1,
				'mode_time': 'back_drive',
				'mode_change': 'on',
				'nevod': 100


				 }


sshem_dict = {'local_path': 'vkontakte_group213575262',
				 'list_question': [['алертность', 'off'], ['отношения в семье', 'off'], ['удача', 'off']],
			  'question_hard':['алертность', 'отношения в семье', 'удача'],
				 'max_len_text': 950,
				 'latitude': 0,
				 'longitude': 0,
				'list_of_ids': [],
				'cenze': 65,
				'theme_cenze': 130,
				  'mode': 'expert',
			  'count':20,
				 'list_no_words':list_no_words,
						'time_bounded': ['off']
,
				'back_drive': 1,
				'mode_time': 'back_drive',
				'mode_change': 'on',
				'nevod': 100

				 }


revelatio_dict = {'local_path': 'revelatio_resurgam1_tg',
				 'list_question': [['Психотерапевтические отношения', 'off'], ['сопротивление в психотерапии', 'off'], ['долгосрочная психотерапия', 'off'] ,
								   ['отношения с психологом', 'off'], ['выдерживать чувства', 'off'], ['базовые эмоции', 'off'], ['контакт с телом', 'off']],

				'question_hard': ['Психотерапевтические отношения', 'сопротивление в психотерапии', 'долгосрочная психотерапия', 'отношения с психологом',
								  'выдерживать чувства', 'базовые эмоции', 'контакт с телом'],
				 'max_len_text': 850,
				 'latitude': 0,
				 'longitude': 0,
				 'list_of_ids': [],
				 'cenze': 75,
				'theme_cenze': 140,
				  'mode': 'expert',
			  'count':20,
				 'list_no_words':list_no_words,
						'time_bounded': ['off']
,
				'back_drive': 1,
				'mode_time': 'back_drive',
				'mode_change': 'on',

				'nevod': 100

				 }



moihalat_dict = {'local_path': 'moihalat_vk',
				 'list_question': [['именнойподарок', 'off'],
								   ['халатсименем', 'off'],  ['халат', 'off'],
								   ['именнаявышивка', 'off'], ['чтоподаритьмужчине', 'off'], ['юбилей', 'off']
								   , ['чтоподарить', 'off'], ['деньрождения', 'off'], ['деньвлюбленных', 'off'], ['чтоподаритьмужчине', 'off']
								   , ['свадьба', 'off'], ['подарок', 'off'], ['именнойхалат', 'off'], ['подарокмужу', 'off']],
				# 'question_hard': ['мягкая игрушка', 'именная вышивка', 'махровый халат', 'идеи подарков'],
				 'max_len_text': 850,
				 'latitude': 0,
				 'longitude': 0,
				 'list_of_ids': [],
				 'cenze': 40,
				'theme_cenze': 90,
				'zero_cenze': 20,
				'mode': 'expert',
			  	'count':20,
				 'list_no_words':list_no_words,
						'time_bounded': ['off']
,
				'back_drive': 1,
				'mode_time': 'back_drive',
				'mode_change': 'off',

				'nevod': 10

				 }

julia_dict = {'local_path': 'julia_hirokama_553948034',
				# 'list_question': [['украина', 'off']] ,
				# 'question_hard': ['украина'],
				 'list_question': [ ['искусственный интеллект', 'off'],  ['анализ аудитории', 'off'], ['нейросети', 'off'],
									['брендинг', 'off'],  ['визитка', 'off'], ['вспышка на солнце', 'off']],  ## ,
				'question_hard': ['искусственный интеллект',  'анализ аудитории', 'нейросети',
									'брендинг',  'визитка', 'солнце'],
				 'max_len_text': 1000,
				 'latitude': 0,
				'longitude': 0,
				'list_of_ids': [ ],
			  	'cenze': 40,
			  	'theme_cenze': 90, ## 170,
				'zero_cenze': 20,
				'mode': 'expert',
				'count':20,
				 'list_no_words': list_no_words,
						'time_bounded': ['off']
,
				'back_drive': 1,
				'mode_time': 'back_drive',
				'mode_change': 'on',
				'nevod': 30,
				'some_time': {'y': 'some', 'm': '4', 'd': '9'},

				 }


custom_dict = {'local_path': 'julia_hirokama_553948034',
				# 'list_question': [ [' ', 'off']] ,
				 'list_question': [ ['ищу работу python', 'off']],
				'question_hard': ['ищу работу'],
				 'max_len_text': 300,
				 'latitude': 0,
				'longitude': 0,
				'list_of_ids': [],
			  	'cenze': 2,
			  	'theme_cenze': 2, ## 170,
				'zero_cenze': 2,
				'mode': 'expert',
				'count':20,
				 'list_no_words': [],
						'time_bounded': ['off']
,
				'back_drive': 1,
				'mode_time': 'back_drive',
				'mode_change': 'on',
				'nevod': 100,
				'some_time': {'y': 'some', 'm': '4', 'd': '9'},
			   	'fin_score_1': 10,
			   'fin_score_2': 10,
			   'all_score_cenze': 10

				 }



yana_dict = {'local_path': 'brizgi_shampanskogo_tg',
				 'list_question': [  ['искусство', 'off'],   [' тайное общество ', 'off'],
									   ['художник', 'off'], ['эстетика', 'off'],  ['театр', 'off'],  ['аристократия', 'off'],  ['харизма', 'off'],['расследование', 'off'],[
										 'путешествие', 'off'],[ 'арсенал', 'off'],[ 'победа', 'off']
									 ],
				'question_hard': [' ', 'тайное общество', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ' ],
				 'max_len_text': 900,
				 'latitude': 0,
				 'longitude': 0,
				 'list_of_ids': [ ],
			 	'cenze': 84,
			 	'theme_cenze': 150,
			 	'mode': 'expert',
				'count':20,
				 'list_no_words':list_no_words,
						'time_bounded': ['off']
,
				'back_drive': 1,
				'mode_time': 'back_drive',
				'mode_change': 'on',
				'nevod': 30


				 }

radiogordost_dict = {'local_path': 'radiogordost_tg',
				 'max_len_text': 2000,
				 'latitude': 0,
				 'longitude': 0,
				 'list_of_ids': [ ],
				# 'dict_for_list_question':{'off': {1: ['17 апреля'], #, '2 апреля','3 апреля','4 апреля','5 апреля','6 апреля','7 апреля','8 апреля'
				# 								  2: [''] }},
				'question_hard': [],
			 	'cenze': 36,
										     #'dict_for_list_question':{'off': {1: ['россия'], 2: ['событие', 'открытие', 'победа', 'премьера', 'гордость',						 'достижение', 'успех', 'признание', 'великий', 'новый', 'первый']}},			'cenze': 84,
				'theme_cenze': 80,
				'zero_cenze' : 12,
				'mode': 'expert',
					'count': 200,
				'list_no_words': ['умер', 'ушёл из жизни', 'умерла', 'ушла из жизни', 'со дня смерти', 'со дня гибели', 'скоропостижн', 'ушел из жизни', '17 апреля 2021',  '17 апреля 2022',  '17 апреля 2023', 'скончал'],
				'time_bounded': ['on', ['past']],
				'back_drive': 50,
				'mode_change': 'off',
				'mode_time': 'some_time',
				'nevod': 100,
				'some_time': {'y': 'some', 'm': '4', 'd': '17'},


					 }


# id_us = -53559272
# group_n = -53559272

emoji_pattern = re.compile("["
							   u"\U0001F600-\U0001F64F"  # emoticons
							   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
							   u"\U0001F680-\U0001F6FF"  # transport & map symbols
							   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
							   u"\U0001F1F2-\U0001F1F4"  # Macau flag
							   u"\U0001F1E6-\U0001F1FF"  # flags
							   u"\U0001F600-\U0001F64F"
							   u"\U00002702-\U000027B0"
							   u"\U000024C2-\U0001F251"
							   u"\U0001f900-\U0001f937"
							   u"\U0001f7e5"
							   u"\U0001F1F2"
							   u"\U0001F1F4"
							   u"\U0001F620-\U0001f7e3"
							   u"\U0001f900-\U0001f9e1"
							   u"\u2000-\u2642"
							   u"\u0300-\u03bf"
							   u"\u203c"
							   "]+", flags=re.UNICODE)
def smails(x):

    return x.translate({ord(i): None for i in smail})

# smails('Привет👋')

def remove_emojis(text):
	# Удаляем все эмодзи из текста
	# clean_text = ''.join(char for char in text if char not in emoji.UNICODE_EMOJI)
	clean_text = smails(text)

	return clean_text


def screening(input_dict, list_question=[''], mode_public='vk'):
	list_of_ids = input_dict['list_of_ids']
	local_path = input_dict['local_path']
	max_len_text = input_dict['max_len_text']
	mode = input_dict['mode']
	try:
		fin_score_1 = input_dict['fin_score_1']
		fin_score_2 = input_dict['fin_score_2']
	except:
		fin_score_1 = 85
		fin_score_2 = 75
	if list_question == ['']:
		try:
			print(input_dict)

			list_question = []
			question_hard_list = []
			for item_1 in input_dict['dict_for_list_question']['off'][1]:
				for item_2 in input_dict['dict_for_list_question']['off'][2]:
					list_question.append([f'{item_1} {item_2}', 'off'])
					question_hard_list.append(item_1)
			input_dict['question_hard'] = question_hard_list

		except:

			list_question = input_dict['list_question']
			# input_dict['question_hard'] = [x[0] for x in input_dict['list_question']]

	print(list_question)


	post_table = pd.DataFrame(
		columns=['public', 'date', 'timestamp', 'attachments', 'likes', 'shares', 'comments', 'views', 'text',  'link',  'geo', 'report',
				  'request' , 'all_score','base_match', 'zero_match','base_perc','zero_perc','ess_perc','dis_perc', 'res_dir', 'res_dis'  ])
	cur_time = time.time()

	for id_us in list_of_ids:
		if mode_public == 'vk':
			base_table = vk_pars_posts_quick.get_public_and_return_base_table_last_day(id_us, id_us, max_len_text=max_len_text)
		base_table['report'] = ''
		base_table['all_score'] = 0
		base_table['request'] = 'Нет специального запроса'
		base_table['base_match'] = 0
		base_table['zero_match'] = 0
		base_table['base_perc'] = 0
		base_table['zero_perc'] = 0
		base_table['ess_perc'] = 0
		base_table['dis_perc'] = 0



		for ind in base_table.index:
			print(ind)
			try:
				len_text = len(base_table.loc[ind, 'text'].split())
				if len_text < max_len_text and base_table.loc[ind, 'text'][:100] not in ' '.join(list(post_table['text'])):

					# text = emoji_pattern.sub(r'', base_table.loc[ind, "text"])
					# text = emoji.replace_emoji(base_table.loc[ind, "text"], replace=lambda chars, data_dict: chars.encode('ascii',
					# 																			   'ignore').decode())

					text = base_table.loc[ind, "text"]
					# text = remove_emojis(base_table.loc[ind, "text"])
					json_scores = local_check_post.check_and_report_one_post(text,
																			 local_path=local_path, mode='common')
					all_score = int(json_scores['sense_perc'])
					base_score = int(json_scores['base_perc'])
					if all_score > fin_score_2 and base_score > fin_score_1:
						print(all_score)
						base_table.loc[ind, 'report'] = json_scores['report']
						base_table.loc[ind, 'all_score'] = all_score
						base_table.loc[ind, 'base_match'] = json_scores['base_match']
						base_table.loc[ind, 'zero_match'] = json_scores['zero_match']
						base_table.loc[ind, 'base_perc'] = json_scores['base_perc']
						base_table.loc[ind, 'zero_perc'] = json_scores['zero_perc']
						base_table.loc[ind, 'ess_perc'] = json_scores['ess_perc']
						base_table.loc[ind, 'dis_perc'] = json_scores['dis_perc']
						print(json_scores['res_dir'], json_scores['res_dis'])
						base_table.loc[ind, 'res_dir'] = json_scores['res_dir']
						base_table.loc[ind, 'res_dis'] = json_scores['res_dis']
						# base_table = base_table[base_table['all_score'] > 0]
						post_table.loc[post_table.shape[0]] = base_table.loc[ind]
						print('post_table.shape', post_table.shape)



			except:
				pass


	## добор длины
	count = 0
	print(post_table)
	print(post_table.shape[0])
	if mode_public == 'vk':
		base_table = vk_pars_posts_quick.get_news_feed_last_day(input_dict, list_question)

	# for question, geo in list_question:
	#
	print(base_table)

	base_table['report'] = ''
	base_table['all_score'] = 0
	base_table['base_match'] = 0
	base_table['zero_match'] = 0
	base_table['base_perc'] = 0
	base_table['zero_perc'] = 0
	base_table['ess_perc'] = 0
	base_table['dis_perc'] = 0

	predict_time_zero = time.time()

	for ind in base_table.index:
		print('ind', ind)
		time_delta_speed = (time.time()-predict_time_zero)/(ind+1)*(base_table.shape[0]-ind+1)
		print('осталось', base_table.shape[0]-ind, 'строк', round(time_delta_speed), 's', round(time_delta_speed/60), 'm',)

		try:
			len_text = len(base_table.loc[ind, 'text'].split())
			if len_text < max_len_text and base_table.loc[ind, 'text'][:100] not in ' '.join(list(post_table['text'])):
				#
				# text = emoji.replace_emoji(base_table.loc[ind, "text"],
				# 						   replace=lambda chars, data_dict: chars.encode('ascii',
				# 																		 'ignore').decode())
				text = base_table.loc[ind, "text"]
				# text = remove_emojis(base_table.loc[ind, "text"])
				json_scores = local_check_post.check_and_report_one_post(text,
																		 local_path=local_path,
																		 mode=mode,
																		 source_dict=input_dict)
				print(json_scores)
				all_score = int(json_scores['sense_perc'])
				try:
					all_score_cenze = input_dict['all_score_cenze']
				except:
					all_score_cenze = 65

				print(all_score_cenze)
				if all_score > all_score_cenze or json_scores['base_perc'] > 60:
					print(all_score)
					base_table.loc[ind, 'report'] = json_scores['report']
					base_table.loc[ind, 'all_score'] = all_score
					base_table.loc[ind, 'base_match'] = json_scores['base_match']
					base_table.loc[ind, 'zero_match'] = json_scores['zero_match']
					base_table.loc[ind, 'zero_match'] = json_scores['zero_match']
					base_table.loc[ind, 'base_perc'] = json_scores['base_perc']
					base_table.loc[ind, 'zero_perc'] = json_scores['zero_perc']
					base_table.loc[ind, 'ess_perc'] = json_scores['ess_perc']
					base_table.loc[ind, 'dis_perc'] = json_scores['dis_perc']
					base_table.loc[ind, 'res_dir'] = int(json_scores['res_dir'])
					base_table.loc[ind, 'res_dis'] = int(json_scores['res_dis'])

					# base_table = base_table[base_table['all_score'] > 0]
					post_table.loc[post_table.shape[0]] = base_table.loc[ind]
					print('post_table.shape', post_table.shape)
				else:
					print('low all_score', all_score)


		except:
			pass
	print(13121, post_table)

	post_table = post_table.sort_values('all_score', ascending=False)
	print(post_table)



	report = ''
	report += f'проверка для паблика {local_path}\n'



	#
	print('o 1 time', time.time() - cur_time)



	# demoji.findall(text)

	for ind in post_table.index:
		print('sec cycle 1', post_table.loc[ind])

		report += '* '*50
		report += '\n'
		report += 'есть геозависимость по запросу' if post_table.loc[ind, "geo"] == 'on' else 'нет геозависимости по запросу \n\n'
		report += f'Запрос: {post_table.loc[ind, "request"]} \n\n'
		# text = demoji.findall(post_table.loc[ind, "text"])
		# text = emoji.replace_emoji(text, replace=lambda chars, data_dict: chars.encode('ascii', 'ignore').decode())
		text = emoji_pattern.sub(r'', post_table.loc[ind, "text"])
		text = smails(text)
		report += text
		report += '\n'
		report += f'Ссылка на источник: {post_table.loc[ind, "link"]} \n'
		# text_rep = demoji.findall(post_table.loc[ind, 'report'])
		# text_rep = emoji.replace_emoji(post_table.loc[ind, 'report'], replace=lambda chars, data_dict: chars.encode('ascii', 'ignore').decode())
		text_rep = post_table.loc[ind, 'report']
		text_rep = emoji_pattern.sub(r'', text_rep)
		# text_rep = smails(text_rep)
		report += text_rep
		report += '\n'

	print('ok time', time.time()-cur_time)

	print(report)
	post_table.to_csv(
		f'F:/learn_neuro/data_vk/{local_path}/post_report/{local_path}_{datetime.datetime.now().date()}.csv')
	with open(f'F:/learn_neuro/data_vk/{local_path}/post_report/{local_path}_{datetime.datetime.now().date()}.txt',
			  'w') as temp:
		temp.write(report)


screening(julia_dict)   #sshem_dict  radiogordost_dict julia_dict  yana_dict  custom_dict
# screening(ymcaprimecenter_dict, 20)


##  list_question=[['крокус', 'off'], ['теракт', 'off']]

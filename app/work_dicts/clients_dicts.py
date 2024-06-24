list_no_words = ['предлага', 'приглаша', 'можете обратиться', 'звоните', 'бесплатн','оплат', 'стоимост', 'подписывайтесь', 'цен', 'расписани', 'марафон', 'руб.', 'все включено']

'как задавать geo:'
"1 - название населенного пункта (string) или 0(int) если ничего"
"2 - регион поиска (['ФО','г', 'обл', 'АО', 'Респ', 'край', 'Аобл'] или 'страна') (string)"
"3 - ранг населенных пунктов (0 - свыше 1 000 000, 1 - свыше 100 000, 2 - свыше 10 000, 3 - все)(int)"



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
				'list_no_words': list_no_words,
				'time_bounded': ['off'],
				'all_score_cenze': 45,
				'back_drive': 1,
				'mode_time': 'back_drive',
				'mode_change': 'on',
				'nevod': 5

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



julia_dict = {'local_path': 'julia_hirokama_553948034',
				# 'list_question': [['украина', 'off']] ,
				# 'question_hard': ['украина'],
				 'list_question': [ ['искусственный интеллект', 'off'],
									['анализ аудитории', 'off'], ['нейросети', 'off'],
									['брендинг', 'off'] ],  ## ,
				'question_hard': ['искусственный интеллект',  'анализ аудитории', 'нейросети',
									'брендинг', ],
				 'max_len_text': 1000,
				 'latitude': 0,
				'longitude': 0,
				'list_of_ids': [ ],
			  	'cenze': 25,
			  	'theme_cenze': 40, ## 90,
				'zero_cenze': 20,
				'mode': 'expert',
				'count': 20,
				 'list_no_words': list_no_words,
						'time_bounded': ['off'],
				'back_drive': 1,
				'mode_time': 'back_drive',
				'mode_change': 'off',
				'nevod': 2,
				'some_time': {'y': 'some', 'm': '4', 'd': '9'},
			  	'all_score_cenze': 65

				 }


custom_dict = {'local_path': 'julia_hirokama_553948034',
				# 'list_question': [ [' ', 'off']] ,
				 'list_question': [ ['ищу квартиру', 'on', ['Сочи', 'край', 2]], ['ищу жилье', 'on', ['Сочи', 'край', 2]],
									['сниму квартиру', 'on', ['Сочи', 'край', 2]]],
				'question_hard': ['ищу квартиру', 'ищу жилье', 'сниму квартиру'],
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
				'mode_change': 'off',
				'nevod': 100,
				'some_time': {'y': 'some', 'm': '4', 'd': '9'},
			   	'fin_score_1': 10,
			   'fin_score_2': 10,
			   'all_score_cenze': 10

				 }




radiogordost_dict = {'local_path': 'radiogordost_tg',
				 'max_len_text': 2000,
				 'latitude': 0,
				 'longitude': 0,
				 'list_of_ids': [ ],
				'list_question': [['событие', 'on', ['Россия', 'Страна', 1]], ['открытие', 'on', ['Россия', 'Страна', 1]],
									['победа', 'on', ['Россия', 'Страна', 1]],['премьера', 'on', ['Россия', 'Страна', 1]],
									['гордость', 'on', ['Россия', 'Страна', 1]]],

				# 'dict_for_list_question':{'off': {1: ['17 апреля'], #, '2 апреля','3 апреля','4 апреля','5 апреля','6 апреля','7 апреля','8 апреля'
				# 								  2: [''] }},
				'question_hard': ['событие', 'открытие', 'победа', 'премьера', 'гордость'],
			 	'cenze': 36,
										     #'dict_for_list_question':{'off': {1: ['россия'], 2: ['событие', 'открытие', 'победа', 'премьера', 'гордость',						 'достижение', 'успех', 'признание', 'великий', 'новый', 'первый']}},			'cenze': 84,
				'theme_cenze': 70,
				'zero_cenze' : 12,
				'mode': 'expert',
					'count': 20,
				'list_no_words': ['умер', 'ушёл из жизни', 'умерла', 'ушла из жизни', 'со дня смерти', 'со дня гибели', 'скоропостижн', 'ушел из жизни', '17 апреля 2021',  '17 апреля 2022',  '17 апреля 2023', 'скончал'],
				'time_bounded': ['on', ['past']],
				'back_drive': 1,
				'mode_change': 'off',
				'mode_time': 'back_drive',
				'nevod': 1,
				'some_time': {'y': 'some', 'm': '4', 'd': '17'},


				}

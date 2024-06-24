# http://opencorpora.org/dict.php?act=gram
# https://pymorphy2.readthedocs.io/en/0.2/user/index.html

import pymorphy2

morph = pymorphy2.MorphAnalyzer()
import pandas as pd
import os


def clean_trash_words(list_words):
	list_trash = ['казахстанец', 'прохвост']
	out_list = [x for x in list_words if x not in list_trash]
	return out_list


def text_clean(text1):
	text2 = text1.replace(
		'(', ' ').replace(
		')', ' ').replace(
		'*', '').replace(
		'[', ' ').replace(
		']', '').replace(
		'\n', ' ').replace(
		'\n', ' ').replace(
		'\ufeff', '').replace(
		'1', '').replace(
		'2', '').replace(
		'3', '').replace(
		'4', '').replace(
		'5', '').replace(
		'6', '').replace(
		'7', '').replace(
		'8', '').replace(
		'9', '').replace(
		'0', '').replace(
		'»', '').replace(
		'«', '').replace(
		'\xa0–', '').replace(
		'–\xa0', '').replace(
		'\xa0', '').replace(
		'\\r', '').replace(
		'\\r\\r', '').replace(
		'\r\r', '').replace(
		'\r', '').replace(
		'\\', '').replace(
		'"', ''
	)
	# text2 = text2.split()
	return text2


def text_clean_for_word_check(text1):
	text2 = text1.replace(
		'(', ' ').replace(
		')', ' ').replace(
		'*', '').replace(
		'[', ' ').replace(
		']', '').replace(
		'\n', ' ').replace(
		'\n', ' ').replace(
		'\ufeff', '').replace(
		'1', '').replace(
		'2', '').replace(
		'3', '').replace(
		'4', '').replace(
		'5', '').replace(
		'6', '').replace(
		'7', '').replace(
		'8', '').replace(
		'9', '').replace(
		'0', '').replace(
		'»', '').replace(
		'«', '').replace(
		'\xa0–', '').replace(
		'–\xa0', '').replace(
		'\xa0', '').replace(
		'\\r', '').replace(
		'\\r\\r', '').replace(
		'\r\r', '').replace(
		'\r', '').replace(
		'\\', '').replace(
		'-', '').replace(
		'"', '').replace(
		'""', ''
	)
	# text2 = text2.split()
	return text2


vision = 1


def reparse_phrase(textBlock, vision=vision):
	# cur_time = time.time()
	all_heros = pd.DataFrame()
	for cutter in range(textBlock.loc[4].max() + 1):

		# delta_time = time.time() - cur_time
		# current_proc1 = round(cutter/((textBlock.loc[4].max() + 1)/100))
		# if current_proc1%20 == 0 and current_proc1 != 0:
		#     print(current_proc1)
		#     print(f'затрачено времени {round(delta_time)}s = {round(delta_time/60)}m ')
		#     print(f'остается {round(delta_time / (current_proc1+0.01) * 100 )}s = {round(delta_time /(current_proc1+0.01)*100/60)}m')

		columns_for_drop = [x for x in textBlock.columns if textBlock[x][4] != cutter]
		text_base = textBlock.drop(columns=columns_for_drop, axis=0)

		if vision:
			print('next_base, phase1')
			print(text_base)
		if list(text_base.columns) != []:
			heros = pd.DataFrame()

			## герои / объекты
			for i in text_base.columns:
				if vision:
					print('next column', text_base[i])

				if text_base[i][1] == 'NOUN':
					if text_base[i][2] == 'nomn':
						heros[i] = text_base[i]
					elif text_base[i][2] == 'accs' or text_base[i][2] == 'gent':
						word_form = text_base[i][5]
						p = morph.parse(word_form)[0]
						acc_word = p.inflect({'nomn', text_base[i][6]}).word
						if vision:
							print('test acc or gen but nomn')
							print(word_form, acc_word)
						### если формы совпадают, надо доп проверить что это герой, а не просто так его плюсовать
						if word_form.lower() == acc_word:

							# проверяем, если нет соседних прилагательных неименительных, это считаем объект если нет герой
							to_obj_ball = 0
							try:
								if text_base[i - 1][1] == 'ADJF' and text_base[i - 1][2] != 'nomn':
									to_obj_ball += 1
							except:
								pass

							try:
								if text_base[i + 1][1] == 'ADJF' and text_base[i + 1][2] != 'nomn':
									to_obj_ball += 1
							except:
								pass

							if to_obj_ball == 0:
								if vision:
									print('heros+')
								list_heros = text_base[i]
								heros[i] = list_heros
								heros[i][3] += 0.5

							else:
								if vision:
									print('obj')
								textBlock[i][3] = 'obj'


						else:
							if vision:
								print('obj')
							textBlock[i][3] = 'obj'

					else:
						if vision:
							print('obj')
						textBlock[i][3] = 'obj'

				elif text_base[i][1] == 'NPRO':  # местоимение, чаще всего будет существительным в контексте
					if text_base[i][2] == 'nomn':
						list_heros = text_base[i]
						heros[i] = list_heros
						try:
							old_hero = all_heros[all_heros.columns[-1]]
							if vision:
								print('old_hero', old_hero)
							if old_hero[6] == heros[i][6] and old_hero[8] == heros[i][8]:
								heros[i][3] += 1
						except:
							if vision:
								print('не вышло получить альхеросов')
							pass
					else:
						if vision:
							print('obj')
						textBlock[i][3] = 'obj'

				elif text_base[i][1] == 'ADJF' and text_base[i][2] == 'nomn':
					list_heros = text_base[i]
					heros[i] = list_heros
					heros[i][3] += 0.5

			# TODO неправильный разбор у них, морозные ночи разобрало как генетив, а не как множественное число. вот с этим что делать.

			# проверки
			# первая по сказуемому
			if vision:
				print('assert hero and deals')
			deals = pd.DataFrame()
			for i in text_base.columns:
				if text_base[i][1] == 'VERB':
					if vision:
						print('deal', text_base[i])
					list_deals = text_base[i]
					deals[i] = list_deals
					number = deals[i][6]
					for j in heros.columns:
						if heros[j][6] == number:
							heros[j][3] += 1
						else:
							heros[j][3] -= 1
					if vision:
						print('deal')
					textBlock[i][3] = 'deal'
				if text_base[i][1] == 'INFN':
					if vision:
						print('deal')
					textBlock[i][3] = 'deal'

			# вторая по винительному падежу
			for i in heros.columns:
				word_form = heros[i][5]
				p = morph.parse(word_form)[0]
				try:
					acc_word = p.inflect({'accs', heros[i][6]}).word
					if heros[i][5].lower() != acc_word:
						heros[i][3] += 0.5
					else:
						if p.tag.animacy == 'anim':
							heros[i][3] += 0.5
						else:
							heros[i][3] -= 0.5
				except:
					pass

			if vision:
				print('heros: ')
				print(heros)

			# забираем максимально вероятных
			for i in heros.columns:
				try:
					max_rate_hero = heros.loc[3].max()
					if heros[i][3] > 0:
						textBlock[i][3] = 'hero'
						hero_list = list(textBlock[i])
						hero_block = pd.DataFrame
						hero_block[i] = hero_list
						textBase = pd.concat([all_heros, hero_block], axis=1)
					else:
						if textBlock[i - 1][1] == 'CONJ':
							if vision:
								print('adjdeal')
							textBlock[i - 1][3] = 'adjdeal'
							textBlock[i][3] = 'adjdeal'
						else:
							if vision:
								print('obj')
							textBlock[i][3] = 'obj'
				except:
					pass

			# разбираем прилагательные и причастия
			if vision:
				print('phase pril')

			for i in text_base.columns:
				if vision:
					print(text_base[i])
				if text_base[i][1] == 'ADVB' or text_base[i][1] == 'GRND':
					if vision:
						print('adjdeal')
					textBlock[i][3] = 'adjdeal'

				elif text_base[i][1] == 'ADJF':
					if vision:
						print(text_base[i][5])
					if text_base[i][2] == 'nomn':
						try:
							text_base[i][6] == all_heros[all_heros.columns[-1]][6]

							if text_base[i][6] == all_heros[all_heros.columns[-1]][6]:
								if text_base[i][8] == all_heros[all_heros.columns[-1]][8]:
									if vision:
										print('adjhero')
									textBlock[i][3] = 'adjhero'
								else:
									if vision:
										print('adjobj')
									textBlock[i][3] = 'adjobj'
							else:
								if vision:
									print('adjobj')
								textBlock[i][3] = 'adjobj'
						except:
							pass


					else:
						if vision:
							print('adjobj')
						textBlock[i][3] = 'adjobj'

			if vision:
				print('перед самой ошибкой', text_base)

			if vision:
				print('changed_block')
				print(textBlock.drop(columns=columns_for_drop, axis=0))

	return textBlock


def encodeTextRazmetka(text, name='str', vision=0):  # текст в список списков с разделителями /
	# cur_time = time.time()
	textBlock = []
	textList = []
	textNumber = []

	text = text_clean(text)

	textBase = pd.DataFrame()
	n = 0
	word = ''
	status = ''
	morph = pymorphy2.MorphAnalyzer()
	exceptList = ['деньги', 'очки']
	not_index = 0

	for index, i in enumerate(text):
		if (index - 1) % 10000 == 0 and index != 1:
			if os.path.isfile(f'{name}{index + 9999}.csv'):
				print(f'{name}{index + 9999}.csv есть в базе')
				not_index = index  #
	for index, i in enumerate(text):
		if index >= not_index:
			# delta_time = time.time() - cur_time
			# current_proc = round(index / ((len(text)) / 100))
			# # print(f'{index} / {len(text)}')
			# if current_proc % 20 == 0 and current_proc!=0 :
			#     print(current_proc)
			#     print(f'затрачено времени {round(delta_time)}s = {round(delta_time/60)}m ')
			#     print(
			#         f'остается {round(delta_time / (current_proc+0.01) * 100 )}s = {round(delta_time /(current_proc+0.01)*100/60)}m')

			if i == '/' or i == '?' or i == '!' or i == '…' or i == '.' or i == ';' or i == ':' or i == '—' or index == len(
					text) - 1:  # or i == ','  ()
				if index == len(text) - 1 and i != '?' and i != '/' and i != '.' and i != ';' and i != ':' and i != '!':
					word = str(word) + i

				if len(word) > 0:
					rawWord = word
					p = morph.parse(word)[0]
					status = 0

					if word not in exceptList:
						word = morph.parse(word)[0].normal_form

					list_for_base = [word, p.tag.POS, p.tag.case, status, len(textList), rawWord, p.tag.number,
									 p.tag.animacy,
									 p.tag.gender, p.tag.involvement, p.tag.voice, p.tag.transitivity, p.tag.tense,
									 p.tag.aspect, p.tag.mood, p.tag.person]

					for i, list_item in enumerate(list_for_base):
						# print(list_item)
						if str(list_item) == 'None':
							list_for_base[i] = 0
						elif str(list_item) != str(list_item):
							list_for_base[i] = 0

					data_list = pd.DataFrame()
					data_list[n] = list_for_base

					textBase = pd.concat([textBase, data_list], axis=1)

					# textBase[n] = [word, p.tag.POS, p.tag.case, status, len(textList), rawWord, p.tag.number, p.tag.animacy,
					#                p.tag.gender, p.tag.involvement, p.tag.transitivity, p.tag.tense,
					#                p.tag.aspect, p.tag.mood]
					status = ''

					textBlock.append(word)
					textNumber.append(n)

					n = n + 1
					word = ''

				# свой разбор предложения

				textList.append(textBlock)
				textBlock = []



			elif i == ' ' or i == ',' or i == '"' or i == '-':
				if len(word) > 0:
					rawWord = word

					# герой и действие
					p = morph.parse(word)[0]
					status = 0

					if word not in exceptList:
						word = morph.parse(word)[0].normal_form

					list_for_base = [word, p.tag.POS, p.tag.case, status, len(textList), rawWord, p.tag.number,
									 p.tag.animacy,
									 p.tag.gender, p.tag.involvement, p.tag.voice, p.tag.transitivity, p.tag.tense,
									 p.tag.aspect, p.tag.mood, p.tag.person]

					for i, list_item in enumerate(list_for_base):
						if str(list_item) == 'None':
							list_for_base[i] = 0

					data_list = pd.DataFrame()
					data_list[n] = list_for_base
					try:
						textBase = pd.concat([textBase, data_list], axis=1)
					except:
						textBase[n] = list_for_base

					# textBase[n] = list_for_base

					# textBase[n] = [word, p.tag.POS, p.tag.case, status, len(textList), rawWord, p.tag.number, p.tag.animacy,
					#                p.tag.gender, p.tag.involvement, p.tag.voice, p.tag.transitivity, p.tag.tense,
					#                p.tag.aspect, p.tag.mood]
					status = ''

					textBlock.append(word)
					textNumber.append(n)

					n = n + 1
					word = ''

			else:  # тут наверное можно дать ей сразу списком знаки
				word = str(word) + i

		# textBase = reparse_phrase(textBase, vision=vision)

		# if index%10000 == 0 and index !=0:
		#     print(current_proc)
		#     print(f'затрачено времени {round(delta_time)}s = {round(delta_time / 60)}m ')
		#     print(
		#         f'остается {round(delta_time / (current_proc + 0.01) * 100)}s = {round(delta_time / (current_proc + 0.01) * 100 / 60)}m')
		#     print('reparce')
		#     textBase = reparsе_phrase(textBase, vision=vision)
		#
		#     textBase.to_csv(f'{name}{index}.csv')
		#     textBase = pd.DataFrame()
		#     textList = []
		#

	return textList, textBase


def encodeTextRazmetka_reparce(text, name='str', vision=0):  # текст в список списков с разделителями /
	# cur_time = time.time()
	textBlock = []
	textList = []
	textNumber = []

	text = text_clean(text)

	textBase = pd.DataFrame()
	n = 0
	word = ''
	status = ''
	morph = pymorphy2.MorphAnalyzer()
	exceptList = ['деньги', 'очки']
	not_index = 0

	for index, i in enumerate(text):
		if (index - 1) % 10000 == 0 and index != 1:
			if os.path.isfile(f'{name}{index + 9999}.csv'):
				print(f'{name}{index + 9999}.csv есть в базе')
				not_index = index  #
	for index, i in enumerate(text):
		if index >= not_index:
			# delta_time = time.time() - cur_time
			# current_proc = round(index / ((len(text)) / 100))
			# # print(f'{index} / {len(text)}')
			# if current_proc % 20 == 0 and current_proc!=0 :
			#     print(current_proc)
			#     print(f'затрачено времени {round(delta_time)}s = {round(delta_time/60)}m ')
			#     print(
			#         f'остается {round(delta_time / (current_proc+0.01) * 100 )}s = {round(delta_time /(current_proc+0.01)*100/60)}m')

			if i == '/' or i == '?' or i == '!' or i == '…' or i == '.' or i == ';' or i == ':' or i == '—' or index == len(
					text) - 1:  # or i == ','  ()
				if index == len(text) - 1 and i != '?' and i != '/' and i != '.' and i != ';' and i != ':' and i != '!':
					word = str(word) + i

				if len(word) > 0:
					rawWord = word
					p = morph.parse(word)[0]
					status = 0

					if word not in exceptList:
						word = morph.parse(word)[0].normal_form

					list_for_base = [word, p.tag.POS, p.tag.case, status, len(textList), rawWord, p.tag.number,
									 p.tag.animacy,
									 p.tag.gender, p.tag.involvement, p.tag.voice, p.tag.transitivity, p.tag.tense,
									 p.tag.aspect, p.tag.mood, p.tag.person]

					for i, list_item in enumerate(list_for_base):
						# print(list_item)
						if str(list_item) == 'None':
							list_for_base[i] = 0
						elif str(list_item) != str(list_item):
							list_for_base[i] = 0

					data_list = pd.DataFrame()
					data_list[n] = list_for_base

					textBase = pd.concat([textBase, data_list], axis=1)

					# textBase[n] = [word, p.tag.POS, p.tag.case, status, len(textList), rawWord, p.tag.number, p.tag.animacy,
					#                p.tag.gender, p.tag.involvement, p.tag.transitivity, p.tag.tense,
					#                p.tag.aspect, p.tag.mood]
					status = ''

					textBlock.append(word)
					textNumber.append(n)

					n = n + 1
					word = ''

				# свой разбор предложения

				textList.append(textBlock)
				textBlock = []



			elif i == ' ' or i == ',' or i == '"' or i == '-':
				if len(word) > 0:
					rawWord = word

					# герой и действие
					p = morph.parse(word)[0]
					status = 0

					if word not in exceptList:
						word = morph.parse(word)[0].normal_form

					list_for_base = [word, p.tag.POS, p.tag.case, status, len(textList), rawWord, p.tag.number,
									 p.tag.animacy,
									 p.tag.gender, p.tag.involvement, p.tag.voice, p.tag.transitivity, p.tag.tense,
									 p.tag.aspect, p.tag.mood, p.tag.person]

					for i, list_item in enumerate(list_for_base):
						if str(list_item) == 'None':
							list_for_base[i] = 0

					data_list = pd.DataFrame()
					data_list[n] = list_for_base
					try:
						textBase = pd.concat([textBase, data_list], axis=1)
					except:
						textBase[n] = list_for_base

					# textBase[n] = list_for_base

					# textBase[n] = [word, p.tag.POS, p.tag.case, status, len(textList), rawWord, p.tag.number, p.tag.animacy,
					#                p.tag.gender, p.tag.involvement, p.tag.voice, p.tag.transitivity, p.tag.tense,
					#                p.tag.aspect, p.tag.mood]
					status = ''

					textBlock.append(word)
					textNumber.append(n)

					n = n + 1
					word = ''

			else:  # тут наверное можно дать ей сразу списком знаки
				word = str(word) + i

	textBase = reparse_phrase(textBase, vision=vision)

	# if index%10000 == 0 and index !=0:
	#     print(current_proc)
	#     print(f'затрачено времени {round(delta_time)}s = {round(delta_time / 60)}m ')
	#     print(
	#         f'остается {round(delta_time / (current_proc + 0.01) * 100)}s = {round(delta_time / (current_proc + 0.01) * 100 / 60)}m')
	#     print('reparce')
	#     textBase = reparsе_phrase(textBase, vision=vision)
	#
	#     textBase.to_csv(f'{name}{index}.csv')
	#     textBase = pd.DataFrame()
	#     textList = []
	#

	return textList, textBase


def encode_text(text):  # текст в список просто весь

	textList = []
	word = ''
	text = text.replace(',', '').replace('.', '').replace(':', '').replace(';', '').replace('!', '').replace('?',
																											 '').replace(
		'…', '')
	textList = text.split()
	# print(textList)
	# for index, i in enumerate(text):
	#     if i != ',' and i != ' ':
	#         word = str(word) + i
	#     if index == len(text) - 1 or i == ',' or i == ' ' or i == '.':
	#         if word != ' ':
	#             textList.append(word)
	#             word = ''

	morph = pymorphy2.MorphAnalyzer()

	# exceptList = ['деньги', 'очки']
	exceptList = [ ]
	textList1 = []
	lat_alpa = [x for x in 'QWERTYUIOPASDFGHJKLZXCVVBNMqwertyuiopasdfghjklzxcvbnm']
	for word in textList:

		if word[0] in lat_alpa:
			word = translate(word)
		# print(word)

		if word not in exceptList:
			try:
				word1 = morph.parse(word)[0].normal_form
				if word1 != '':
					textList1.append(word1)
			except:
				textList1.append(word)

	return textList1


def encode_text_without_normalize(text):  # текст в список просто весь

	textList = []
	word = ''
	text = text.replace(',', '').replace('.', '').replace(':', '').replace(';', '').replace('!', '').replace('?',
																											 '').replace(
		'…', '')
	text = text.replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5',
																											 '').replace(
		'6', '')
	text = text.replace('7', '').replace('8', '').replace('9', '')
	textList = text.split()
	# for index, i in enumerate(text):
	#     if i != ',' and i != ' ':
	#         word = str(word) + i
	#     if index == len(text) - 1 or i == ',' or i == ' ' or i == '.':
	#         if word != ' ':
	#             textList.append(word)
	#             word = ''

	morph = pymorphy2.MorphAnalyzer()

	exceptList = ['деньги', 'очки']
	textList1 = []
	lat_alpa = [x for x in 'QWERTYUIOPASDFGHJKLZXCVVBNMqwertyuiopasdfghjklzxcvbnm']
	for word in textList:

		if word[0] in lat_alpa:
			word = translate(word)
		# print(word)

		# if word not in exceptList:
		#     word = morph.parse(word)[0].normal_form
		if word != '':
			textList1.append(word)
	# textList1.append(word)
	return textList1



def encode_text_without_normalize_with_numbers(text):  # текст в список просто весь
	print(text)

	textList = []
	word = ''
	text = text.replace(',', '').replace('.', '').replace(':', '').replace(';', '').replace('!', '').replace('?',
																											 '').replace(
		'…', '')
	# text = text.replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5',
	# 																										 '').replace(
	# 	'6', '')
	# text = text.replace('7', '').replace('8', '').replace('9', '')
	textList = text.split()
	print(textList)
	# for index, i in enumerate(text):
	#     if i != ',' and i != ' ':
	#         word = str(word) + i
	#     if index == len(text) - 1 or i == ',' or i == ' ' or i == '.':
	#         if word != ' ':
	#             textList.append(word)
	#             word = ''

	morph = pymorphy2.MorphAnalyzer()

	exceptList = ['деньги', 'очки']
	textList1 = []
	lat_alpa = [x for x in 'QWERTYUIOPASDFGHJKLZXCVVBNMqwertyuiopasdfghjklzxcvbnm']
	for word in textList:

		if word[0] in lat_alpa:
			try:
				word1 = morph.parse(translate(word1))[0].normal_form
				word = translate(word)
			except:
				pass
		# print(word)

		# if word not in exceptList:
		#     word = morph.parse(word)[0].normal_form
		if word != '':
			textList1.append(word)
	# textList1.append(word)
	return textList1


def translate(word):
	list_word = []
	list_en = ['A', 'B', 'E', 'Z1', 'Z', 'I', 'K', 'L', 'M', 'H', 'O', 'PP', 'P', 'C', 'T', 'U', 'X']
	list_rus = ['а', 'в', 'е', 'ж', 'з', 'и', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'х']
	for letter in word:
		for i, en_let in enumerate(list_en):
			if letter == en_let:
				list_word.append(list_rus[i])

	word = ''.join(list_word)
	return word


def check_word(word):
	# исключения нужны для убирания мусорных частей речи и слов

	except_list = ['PREP', 'NPRO', 'CONJ', 'INFN', 'PRTS', 'GRND', 'PRTF', 'NUMR', 'PRCL', 'INTJ', 'ADVB', 'PRED']
	except_list1 = [
		'опыт', 'знание', 'понимание', 'работа', 'год', '3‐х', 'х', 'умение', 'владение',
		'сложный', 'запрос', 'больший', ' ', 'использование', 'должный', 'естественный', 'хороший',
		'новый', 'большой', 'плюс', 'любой', 'команда', 'обучение', 'знакомство', 'связанный', 'часть',
		'способность', 'желание', 'такой', 'связанный', 'желательный', 'помощь',
		'развитие', 'митап', 'встреча', 'сам', 'отличный', 'преимущество', 'базовый', 'который',
		'митап', 'тема', 'обмен', 'актуальный', 'внутренний', 'архитектурный', 'возможность',
		'профессиональный', 'полный', 'частичный', 'практика', 'документация', 'чтение', 'достаточный',
		'тот', 'этот', 'уровень', 'библиотека', 'наличие', 'проект', 'background',
		'обертка', 'встраивание', 'обернуть', 'встроить', 'обёртка', 'написание', 'подход', 'последующая',
		'миграция', 'отдельный', 'компания', 'разработчик', 'иной', 'другой', 'качественный', 'практический',
		'поддержание', 'уверенный', 'конкурентный', 'семейство', 'свой',
		'код', 'высокий', 'принцип', 'особенность', 'построение', 'портфолио', 'упорство', 'продуктивность', '3х'
	]
	if not str(word[0]).isdigit() and word[0] not in except_list1 and word[1] not in except_list:
		return True


def normalize_text(text_list):
	norm_list = []
	morph = pymorphy2.MorphAnalyzer()
	for word in text_list:
		try:
			norm_list.append(morph.parse(word)[0].normal_form)
		except:
			pass
	return norm_list


def return_word(word_series):
	# списки индексов изменяемых признаков, актуальных для pymorphy
	indexed_aspect_dict = {'NOUN': [1, 3], 'VERB': [3, 5, 6, 7, 9, 10, 11], 'ADVB': [], 'PRTS': [1, 3, 5, 7, 9, 10],
						   'CONJ': [], 'PREP': [], 'NPRO': [1, 3, 5], 'ADJF': [1, 3, 5], 'INFN': [], 'PRCL': []}

	out_str = []
	print(word_series)
	word_list = [x for x in word_series[0]]
	change_word = 0
	morph_word = morph.parse(word_list[5])[0]
	word_list = word_list[1:4] + word_list[6:]

	# print(word_list)
	list_states = []
	for i, x in enumerate(word_list):

		if i in indexed_aspect_dict[word_list[0]]:
			list_states.append(x)

	# print(list_states)
	list_actual = []
	for state in list_states:
		# print(state)
		try:
			morph_word.inflect({state})
			# print(morph_word.inflect({state}).word)
			list_actual.append(state)

		except:
			pass
	if list_actual:
		change_word = morph_word.inflect({x for x in list_actual})

		out_str.append(change_word.word)
	else:
		out_str.append(word_list[0])

	return out_str


def return_list(table):
	# списки индексов изменяемых признаков, актуальных для pymorphy
	indexed_aspect_dict = {'NOUN': [1, 3], 'VERB': [3, 5, 6, 7, 9, 10, 11], 'ADVB': [], 'PRTS': [1, 3, 5, 7, 9, 10],
						   'CONJ': [], 'PREP': [], 'NPRO': [1, 3, 5], 'ADJF': [1, 3, 5], 'INFN': [], 'PRCL': []}

	out_str = []

	for column in table.columns:
		word_list = [x for x in table[column]]
		# print(word_list)
		morph_word = morph.parse(word_list[5])[0]
		# print(morph_word)
		word_list = word_list[1:4] + word_list[6:]

		# print(word_list)
		list_states = []
		for i, x in enumerate(word_list):

			if i in indexed_aspect_dict[word_list[0]]:
				list_states.append(x)

		# print(list_states)
		list_actual = []
		for state in list_states:
			# print(state)
			try:
				morph_word.inflect({state})
				# print(morph_word.inflect({state}).word)
				list_actual.append(state)

			except:
				pass
		if list_actual:
			try:
				change_word = morph_word.inflect({x for x in list_actual})

				out_str.append(change_word.word)
			except:
				out_str.append(morph_word.normal_form)

		else:
			out_str.append(morph_word.normal_form)

	return out_str


def animal(word):
	try:
		p = morph.parse(word)[0]
		if 'anim' in p.tag:
			return True
		else:
			return False
	except:
		return False


def adj(word):
	try:
		p = morph.parse(word)[0]
		if 'ADJF' in p.tag:
			return True
		else:
			return False
	except:
		return False


def masc(word, sense):
	try:
		p = morph.parse(word)[0]
		word1 = p.inflect({sense[0], 'nomn'})
		return word1.word
	except:
		return word


def n_form(word):
	return morph.parse(word)[0].normal_form


def prtf(word):
	try:
		p = morph.parse(word)[0]
		if 'PRTF' in p.tag or 'PRTS' in p.tag:
			return True
		else:
			return False
	except:
		return False


def adv(word):
	try:
		p = morph.parse(word)[0]

		if 'ADVB' in p.tag:

			return True
		else:
			return False
	except:
		return False


def is_time(word):
	try:
		p = morph.parse(word)[0]

		if 'futr' in p.tag:
			return [0, 0, 1]
		elif 'pres' in p.tag:
			return [0, 1, 0]
		elif 'past' in p.tag:
			return [1, 0, 0]

	except:
		return False


# убрать задвоения
def clean_list_without_changes_form(list_words):
	new_list = []
	for word in list_words:
		if word not in new_list:
			new_list.append(word)

	return new_list

sense_conj_dict = { 1:'причина', 2: 'последствия', 3:'место', 4: 'время', 5: 'положение', 6: 'способ',
						7: 'начало, источник',  8: 'тема', 9: 'цель', 10: 'последовательность', 11: 'два равнозначных'}

def interpretate_CONJ(table):

	conj_dict = {'и': [10, 2, ], 'в': [3, 4], 'с': [7, 6], 'под': [3], 'потому что': [1], 'затем': [10, 4],
				 'для': [2, 9], 'около': [3, 4], 'у': [3, 4], 'на': [3], 'во': [4], 'ведь':  [1], 'за': [1, 3, 6],
				 'перед': [3, 4], 'из': [3, 1], 'из-за': [3, 1], 'к': [9], 'от': [3, 4, 7], 'до': [3, 4, 9],
				 'между': [5], 'когда': [4, 7], 'тогда': [4, 9]}

	conj_list = ['CONJ', 'PREP', 'PRCL']

	table_small = table.drop([col for col in table.columns if table.loc[1, col].lower() in conj_list], axis=1)

	table.loc[16] = 0
	for col in table_small.columns:
		try:
			name_conj = table.loc[0, col].lower()
			table.loc[16, col] = conj_dict[name_conj][0]
			table.loc[3, col] = ''.join([i for i in sense_conj_dict[name_conj]])
		except:
			pass

	return table

def good_match(list_of_words):
	dict_of_parse = {'noun': [], 'count': [], 'gender': [], 'form':[]}

	for word in list_of_words:
		encoded_word = morph.parse(word)
		list_of_tags = str(encoded_word[0].tag).split(sep=',')
		# print(list_of_tags)
		for tag in list_of_tags:
			if tag in ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']:
				dict_of_parse['noun'].append(tag)
			elif tag in ['sing', 'plur']:
				dict_of_parse['count'].append(tag)
			elif tag in ['masc', 'femn', 'neut', 'masc sing', 'Qual femn']:
				dict_of_parse['gender'].append(tag)
			elif tag in ['PREP', 'NPRO', 'CONJ', 'INFN', 'PRTS', 'GRND', 'PRTF', 'NUMR', 'PRCL', 'INTJ', 'ADVB', 'PRED', 'ADJF', 'NOUN', 'VERB']:
				dict_of_parse['form'].append(tag)
	# print(dict_of_parse)
	if len(dict_of_parse['form']) > 1:
		if dict_of_parse['form'][0] != dict_of_parse['form'][1]:
			for key in dict_of_parse.keys():
				if len(dict_of_parse[key]) > 1:
					list_tags = dict_of_parse[key]
					if list_tags[0] == list_tags[1]:
						print('true', list_of_words)
						return True
					else:
						print('false', list_of_words)
						return False

	print('true', list_of_words)
	return True



def get_phrase_and_return_all_forms(phrase):
	out_list = []
	form_list_for_noun = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']
	form_list_for_count = ['sing', 'plur']
	form_list_for_gender = ['masc', 'femn', 'neut']
	form_list_for_time = ['pres', 'past', 'futr']

	# phrase = encode_text_without_normalize(phrase)
	phrase = encode_text_without_normalize_with_numbers(phrase)
	encoded_phrase = [morph.parse(word) if len(morph.parse(word)) > 0 else word for word in phrase]
	for form in form_list_for_count:
		for form_1 in form_list_for_gender:
			for form_2 in form_list_for_noun:
				for form_3 in form_list_for_time:
					mini_list = []
					for word in encoded_phrase:
						try:
							word = word[0]
							if 'NOUN' in word.tag or 'ADJF' in word.tag or 'PRTF' in word.tag:
								try:
									mini_list.append(word.inflect({form, form_1, form_2}).word)
								except:
									mini_list.append(word.word)

							else:
								try:
									mini_list.append(word.inflect({form, form_1, form_3}).word)
								except:
									mini_list.append(word.word)
						except:
							mini_list.append(word)

				if len(mini_list) == len(encoded_phrase):
					if len(mini_list) > 1:
						if good_match(mini_list):
							out_list.append(' '.join(mini_list))

					elif len(mini_list) > 0:
						out_list.append(mini_list[0])

	return list(set(out_list))

# get_phrase_and_return_all_forms('путешествие в икстлан')
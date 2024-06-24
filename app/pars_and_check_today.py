import datetime
import time
import local_check_post   ### todo заменить на api val
import pandas as pd
from app import vk_pars_posts_quick
from news_search_f import f_clean_smiles, f_geo
from work_dicts import clients_dicts



def transform_list_questions(list_of_question_items, question_hard_list_items):

	list_question = []
	question_hard_list = []

	for i, item in enumerate(list_of_question_items):

		if item[1] == 'off':
			list_question.append([item[0], item[1]])
			question_hard_list.append(question_hard_list_items[i])

		else:
			list_of_words = f_geo.find_city(item[2])
			for city in list_of_words:
				list_question.append([f'{item[0]} {city}', 'on'])
				question_hard_list.append(question_hard_list_items[i])



	print('list_question', list_question)
	print('question_hard_list', question_hard_list)

	return list_question, question_hard_list


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

	list_question, question_hard_list = transform_list_questions(input_dict['list_question'], input_dict['question_hard'])
	input_dict['question_hard'] = question_hard_list


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
		text = f_clean_smiles.emoji_pattern.sub(r'', post_table.loc[ind, "text"])
		text = f_clean_smiles.smails(text)
		report += text
		report += '\n'
		report += f'Ссылка на источник: {post_table.loc[ind, "link"]} \n'
		text_rep = post_table.loc[ind, 'report']
		text_rep = f_clean_smiles.emoji_pattern.sub(r'', text_rep)
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


screening(clients_dicts.julia_dict)   #sshem_dict  radiogordost_dict julia_dict  yana_dict  custom_dict
# screening(ymcaprimecenter_dict, 20)



import datetime
import random

import time

import openpyxl as openpyxl
import pandas as pd
import tg_pars
from for_news_search.news_search_f import f_geo
from for_news_search.work_dicts import clients_dicts
from for_news_search.work_dicts.news_dicts import all_ids_dicts
import local_check_post



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


def screening(input_dict, list_question=[''], mode_public='tg'):
	cur_time = time.time()
	date = str(datetime.datetime.now().date())

	local_path = input_dict['local_path']
	max_len_text = input_dict['max_len_text']
	mode = input_dict['mode']


	dict_of_ids_name = f'{local_path[:-3]}_tg_channels_dict'
	print(dict_of_ids_name)
	dict_of_ids = all_ids_dicts[dict_of_ids_name]

	# list_question, question_hard_list = transform_list_questions(input_dict['list_question'], input_dict['question_hard'])
	# input_dict['question_hard'] = question_hard_list

	columns = ['public', 'date', 'timestamp', 'attachments', 'likes', 'shares', 'comments', 'views', 'text', 'link',
			   'geo', 'report',
			   'request', 'all_score', 'base_match', 'zero_match', 'base_perc', 'zero_perc', 'ess_perc', 'dis_perc',
			   'res_dir', 'res_dis', 'exciles']

	post_table = pd.DataFrame(columns=columns)
	predict_time_zero = time.time()
	k = 0.1


	for i, [channel, name] in enumerate(list(dict_of_ids.items())):
		## потытка рандомной паузы
		time.sleep(random.random()*k)
		k += i
		if k > 5:
			if random.random() > 0.5:
				k = 0

		print(f'search for {name}, {i} from {len(dict_of_ids)}')
		if mode_public == 'tg':
			base_table = tg_pars.get_public_and_return_base_table_last_day(channel, name, days_ago=input_dict['back_drive'])
			base_table['report'] = ''
			base_table['all_score'] = 0
			base_table['base_match'] = 0
			base_table['zero_match'] = 0
			base_table['base_perc'] = 0
			base_table['zero_perc'] = 0
			base_table['ess_perc'] = 0
			base_table['dis_perc'] = 0

			for ind in base_table.index:
				print('ind', ind)
				time_delta_speed = (time.time() - predict_time_zero) / (ind + 1) * (base_table.shape[0] - ind + 1)
				print('осталось', base_table.shape[0] - ind, 'строк', round(time_delta_speed), 's',
					  round(time_delta_speed / 60), 'm', )

				len_text = len(base_table.loc[ind, 'text'].split())
				if len_text < max_len_text and base_table.loc[ind, 'text'][:100] not in ' '.join(
						list(post_table['text'])):

					text = base_table.loc[ind, "text"]
					print(text)
					json_scores = local_check_post.check_and_report_one_post(text,
																			 local_path=local_path,
																			 mode=mode,
																			 source_dict=input_dict)
					if json_scores['valid'] != 0:
						print('json_scores', json_scores)
						all_score = int(json_scores['sense_perc'])
						all_score_cenze = input_dict['all_score_cenze']

						print('all_score_cenze', all_score_cenze)
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
							# local_path = work_dict['local_path']
							file_name = f'F:/learn_neuro/data_vk/{local_path}/post_report/{local_path}_{date}.xlsx'
							# resultExcelFile = pd.ExcelWriter(f'F:/learn_neuro/data_vk/{local_path}/post_report/{local_path}_{date}.xlsx')
							post_table.to_excel(file_name)

							print('post_table.shape', post_table.shape)
						else:
							print('low all_score', all_score)

		# post_table = pd.concat([post_table, base_table], axis=0)



	post_table = post_table.sort_values('all_score', ascending=False)
	post_table = post_table.reset_index()

	post_table = post_table.drop(['public', 'timestamp', 'attachments', 'likes', 'shares', 'comments', 'views',
			   'geo', 'report',   'all_score', 'base_match', 'zero_match', 'base_perc', 'zero_perc', 'ess_perc', 'dis_perc',
			   'res_dir', 'res_dis', 'index'], axis=1)

	print(f'завершено, время {time.time() - predict_time_zero} s, {round((time.time() - predict_time_zero)/60)} m')

	return post_table



def csv_to_excel(data, excel_file):

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    for row in data:
        sheet.append(row)
    workbook.save(excel_file)

work_dict = clients_dicts.radiogordost_dict
post_table = screening(work_dict)   #sshem_dict  radiogordost_dict julia_dict  yana_dict  custom_dict
print(post_table)

# local_path = work_dict['local_path']
# file_name = f'F:/learn_neuro/data_vk/{local_path}/post_report/{local_path}_{date}.xlsx'
# # resultExcelFile = pd.ExcelWriter(f'F:/learn_neuro/data_vk/{local_path}/post_report/{local_path}_{date}.xlsx')
# post_table.to_excel(file_name)




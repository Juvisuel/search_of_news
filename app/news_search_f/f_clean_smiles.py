import re
import pandas as pd
smail = pd.read_csv('F:/learn_neuro/emo_bot/docs/smails.csv')
smail = ''.join(list(smail['smail']))

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

import datetime
import pytz


currentTimeZone = pytz.timezone('Europe/Moscow')
print(currentTimeZone)

# работа со штампами времени
# таймштамп из дату (только вида YYYY-MM-DD строка)
def timestamp_from_date(date):
	timestamp = datetime.datetime.strptime(date, "%Y-%m-%d").timestamp()
	return int(timestamp)

# время из таймштампа
def time_from_timestamp(timestamp, timezone):
	time = datetime.fromtimestamp(timestamp).time()
	return time


def extract_int_time_parts_from_str_time(str_time):
	str_list = str_time.split(sep=':')

	time_hours = int(str_list[0])
	time_mins = int(str_list[1])
	try:
		time_sec = int(str_list[2])
	except:
		time_sec = 0

	return time_hours, time_mins, time_sec

def extract_int_time_from_timestamp(timestamp):
	time_hours = datetime.datetime.fromtimestamp(timestamp).hour
	time_mins = datetime.datetime.fromtimestamp(timestamp).minute
	time_secs = datetime.datetime.fromtimestamp(timestamp).second

	return time_hours, time_mins, time_secs


def alert_time_or_not(alert_time, now_time):
	alert_hours, alert_min, alert_secs = extract_int_time_parts_from_str_time(alert_time)
	now_hour, now_min, now_secs = extract_int_time_from_timestamp(now_time)

	alert_time = datetime.datetime(2023, 1, 1, alert_hours, alert_min, alert_secs).timestamp()
	now_time = datetime.datetime(2023, 1, 1, now_hour, now_min, now_secs).timestamp()

	if now_time > alert_time:
		print('время или просрочка')
		return True
	else:
		print('не время')
		return False

def evening_time(now_time):
	time_hours, time_mins, time_secs = extract_int_time_from_timestamp(now_time)
	if time_hours > 19:
		return True
	else:
		return False




# получение временной зоны
def get_timezone(zone_name):
	return pytz.timezone(zone_name)


# проверка "сегодня или нет", принимает штамп времени пользователя и его часовой пояс
def today_or_not(timestamp, zone_name='Europe/Moscow'):
	timezone = pytz.timezone(zone_name)
	date_today = datetime.datetime.now(timezone).date()
	date_to_check = datetime.datetime.fromtimestamp(timestamp).date()
	if date_today == date_to_check:
		return True
	else:
		return False


def in_two_days(session, zone_name='Europe/Moscow'):
	timezone = pytz.timezone(zone_name)
	if not today_or_not(session.last_answer_datetime):
		date_today = datetime.datetime.now(timezone).date()
		date_to_check = datetime.datetime.fromtimestamp(session.last_answer_datetime).date()
		if date_today-date_to_check < 3:
			return True

	return False

def yesterday(session, zone_name='Europe/Moscow'):
	timezone = pytz.timezone(zone_name)
	if not today_or_not(session.last_answer_datetime):
		date_today = datetime.datetime.now(timezone).date()
		date_to_check = datetime.datetime.fromtimestamp(session.last_answer_datetime).date()
		if date_today - date_to_check == 1:
			return True

	return False


def check_hovering_or_active(self, list_session):
	## делать каждый день раз в сутки
	for session in list_session:
		if today_or_not(session.last_answer_datetime) and len(
				session.report) > 0:  # сегодня были ответы, но сессия не завершена
			## todo если уже скорее вечер, стоит напомнить даже статусу активному, пишем проверку на вечер тут
			if evening_time():  # уже вечер, лист для напоминания вечером тем, кто пропустил сегодня
				session.status = 'sleeping'
		elif in_two_days(session.last_answer_datetime):  # не было ответов вчера или позавчера
			session.status = 'hovering'

	return list_session


def calculate_delta_time_min_from_strings(str_time_1, str_time_2):
	time_1_h, time_1_m, time_1_s = extract_int_time_parts_from_str_time(str_time_1)
	time_2_h, time_2_m, time_2_s = extract_int_time_parts_from_str_time(str_time_2)
	i = 0
	if time_2_h < time_1_h: # встаем утром, а ложимся вечером:
		i=1

	time1_timestamp = datetime.datetime(2023, 1, 1, time_1_h, time_1_m, time_1_s).timestamp()
	time2_timestamp = datetime.datetime(2023, 1, 1+i, time_2_h, time_2_m, time_2_s).timestamp()
	print(time2_timestamp, time1_timestamp)
	delta_time = time2_timestamp-time1_timestamp


	return delta_time//60


delta = calculate_delta_time_min_from_strings('10:30', '12:30')
print(delta)

## todo надо чистить все репорты в 0 часов


def in_some_days(timestamp_post, zone_name='Europe/Moscow', days=365):

	timezone = pytz.timezone(zone_name)
	date_today = datetime.datetime.now(timezone).date()
	date_to_check = datetime.datetime.fromtimestamp(timestamp_post).date()

	# date_to_check = datetime.datetime.fromtimestamp(timestamp_post)
	# print('от тогда до сегодня',(date_today - date_to_check).days)
	# print(days)

	if (date_today-date_to_check).days < days:
		return True

	return False


# print(alert_time_or_not('12:30:00', datetime.datetime.now().timestamp()))
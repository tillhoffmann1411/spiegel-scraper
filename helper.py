import os

def rm_empty_lines(string: str) -> str:
  return os.linesep.join([s for s in string.splitlines() if s])

def rm_line_breaks(string: str) -> str:
  return string.replace("\n", " ")

def rm_all_line_breaks(string: str) -> str:
  return rm_line_breaks(rm_empty_lines(string))

def clean_up_string(string: str) -> str:
  return string.replace('\n', '').strip()

def split_up_date(string: str) -> tuple[str, str]:
  cleaned_str = string.replace(' ', '').replace('Uhr', '')
  splited_date_time = cleaned_str.split(',')
  date = splited_date_time[0]
  unsafe_time = splited_date_time[1].replace('.', ':')
  split_time = unsafe_time.split('•')
  if len(split_time) > 1:
    return replace_month(date), split_time[0], split_time[1]
  else:
    return date_reverse(date), split_time[0]

def replace_month(string: str) -> str:
  day_str = string.split('.')[0]
  year_str = string[-4:]
  month_str = string[:-4].split('.')[1]
  month_str_num = {
    'Januar': 1,
    'Februar': 2,
    'März': 3,
    'April': 4,
    'Mai': 5,
    'Juni': 6,
    'Juli': 7,
    'August': 8,
    'September': 9,
    'Oktober': 10,
    'November': 11,
    'Dezember': 12
  }
  return year_str + '-' + str(month_str_num[month_str]) + '-' + day_str;

def date_reverse(date: str) -> str:
  [day, month, year] = date.split('.')
  reversed_date = '-'.join([year, month, day])
  return reversed_date
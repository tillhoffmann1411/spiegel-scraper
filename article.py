from bs4 import BeautifulSoup
import requests

from spiegel_scraper.helper import rm_all_line_breaks, clean_up_string, split_up_date

def get_articels_details(url: str):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    title = clean_up_string(rm_all_line_breaks(soup.find('h2').text))

    author = ''
    try:
        author = clean_up_string(soup.find('a', class_='text-black dark:text-shade-lightest font-bold border-b border-shade-light hover:border-black dark:hover:border-white').text)
    except:
        print('could not parse author for title: ' + title)

    time_element = soup.find('time')
    [date, time] = '', ''

    if time_element != None:
        [date, time] = split_up_date(time_element.text)
        
    
    paragraphs = soup.find_all('p', class_='')
    long_paragraph = map(lambda p: p.text, paragraphs)
    text = clean_up_string(' '.join(long_paragraph))
    
    images = soup.find_all('img', {'class': r'^((?!lazyload).)*$'}) # This does not work - fix this later!
    image_src_lst = list(map(lambda img: img['src'], images))

    return {
        'title': title,
        'author': author,
        'date': date,
        'time': time,
        'text': text,
        'url': url,
        'images': image_src_lst
    }
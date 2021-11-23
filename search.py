from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from spiegel_scraper.helper import clean_up_string, split_up_date


def search(keyword: str, show_browser = False, start_on_page = 1):
  driver = initialize_page('https://www.spiegel.de/suche/?suchbegriff=' + keyword, 'Suche', show_browser)
  handle_cookie_banner(driver)
  max_page_nr = get_max_page(driver)
  articles = []

  for page in range(start_on_page, max_page_nr + 1):
    print('Parse articles of page ' + str(page))
    driver = go_to_url(driver, 'https://www.spiegel.de/suche/?suchbegriff=' + keyword + '&seite=' + str(page), 'Suche')
    # Wait until the articles are loaded
    wait = WebDriverWait(driver, 10)
    wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="suchergebnisse"]/section')))
    new_articles = get_articels_from_page(driver, page, keyword)
    articles = articles + new_articles
    
  driver.close()
  return articles

def get_articels_from_page(driver: WebDriver, page: int, keyword: str):
  article_elements = driver.find_elements(By.CSS_SELECTOR, 'article.lg\:py-24.md\:py-24.sm\:py-16')
  articles = []
  nr = 0
  for article in article_elements:
    title = clean_up_string(article.find_element(By.TAG_NAME, 'header').text)

    if title != '':
      print('parse article ' + str(nr))
      nr += 1
      url = ''
      description = ''
      url = article.find_element(By.TAG_NAME, 'a').get_attribute('href')
      description = clean_up_string(article.find_element(By.TAG_NAME, 'section').text)
      date_time = article.find_elements(By.TAG_NAME, 'span')

      if len(date_time) > 0 and date_time[-1] != '':
        [date, time, category] = split_up_date(date_time[-1].text)

      articles.append({
        'title': title,
        'description': description,
        'category': category,
        'url': url,
        'date': date,
        'time': time,
        'page': page,
        'article_on_page': nr,
        'search_keyword': keyword
      })
  return articles

def handle_cookie_banner(driver: WebDriver):
  # Wait max 10 seconds for cookie-banner to appear
  wait = WebDriverWait(driver, 10)
  wait.until(ec.visibility_of_element_located((By.ID, 'sp_message_iframe_541484')))
  driver.switch_to.frame('sp_message_iframe_541484')
  button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/div[1]/button')
  button.click()
  driver.switch_to.default_content()

def initialize_page(url: str, partial_title = '', headless = True) -> WebDriver:
  options = Options()
  if headless:
    options.headless = True
  driver = webdriver.Chrome('./chromedriver', options=options)
  go_to_url(driver, url, partial_title)
  return driver

def go_to_url(driver: WebDriver,url: str, partial_title = '') -> WebDriver:
  driver.get(url)
  assert partial_title in driver.title
  return driver

def get_max_page(driver: WebDriver) -> int:
  max_page = driver.find_element(By.XPATH, '//*[@id="Inhalt"]/section/nav/div/span/span[2]').text
  return int(max_page)
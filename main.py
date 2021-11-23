from spiegel_scraper.search import search
from spiegel_scraper.article import get_articels_details

import pandas as pd


# Insert here your search keyword!
keyword = 'Spiegel scraper'



def search_articles(keyword: str):
  articles = search(keyword)
  print('Found ' + str(len(articles)) + ' articles')
  return articles

def get_single_article(url: str):
  return get_articels_details(url)

def fetch_all_articles_for_topic(keyword: str):
  article_infos = search_articles(keyword)
  articles = []
  for i, article in enumerate(article_infos):
    article_details = get_single_article(article['url'])
    enhanced_article = {**article, **article_details}
    articles.append(enhanced_article)
  articles_df = pd.DataFrame(articles)
  print(articles_df)
  return articles_df


# articles_df = fetch_all_articles_for_topic(keyword)
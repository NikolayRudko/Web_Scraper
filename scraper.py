import os

import requests
import string
from urllib.parse import urljoin

from bs4 import BeautifulSoup


class NatureScraper:
    articles_info = {"Article": ["div", {"class": "c-article-body"}],
                     "Author Correction": ["div", {"class": "c-article-body"}],
                     "Book Review": ["div", {"class": "c-article-body u-clearfix"}],
                     "Career Column": ["div", {"class": "c-article-body u-clearfix"}],
                     "Comment": ["main", {"class": "c-article-main-column u-float-left"}],
                     "Correspondence": ["div", {"class": "c-article-body u-clearfix"}],
                     "Editorial": ["div", {"class": "c-article-body u-clearfix"}],
                     'Futures': ["main", {"class": "c-article-main-column u-float-left"}],
                     'Nature Briefing': ["div", {"class": "c-article-body u-clearfix"}],
                     'Nature Podcast': ["div", {"class": "c-article-body u-clearfix"}],
                     'News': ["div", {"class": "c-article-body u-clearfix"}],
                     "News & Views": ["p", {"class": "article__teaser"}],
                     "News Feature": ["div", {"class": "c-article-body u-clearfix"}],
                     "News Round-Up": ["div", {"class": "c-article-body u-clearfix"}],
                     "Outlook": ["div", {"class": "c-article-body u-clearfix"}],
                     "Publisher Correction": ["div", {"class": "c-article-body"}],
                     "Research Highlight": ["main", {"class": "c-article-main-column u-float-left"}],
                     "Where I Work": ["div", {"class": "c-article-body"}],
                     "World View": ["div", {"class": "c-article-body"}],
                     }

    def __init__(self, url):
        self.url = url
        self.files = []

    def run(self, articles_type: str, pages: int):
        for i in range(1, pages + 1):
            url = self.url + str(pages)
            req = requests.get(url)
            full_path = f"Page_{str(i)}"
            os.makedirs(full_path, exist_ok=True)
            if req:
                soup = BeautifulSoup(req.content, 'html.parser')
                content = soup.find(id="content").find_all('article', class_="u-full-height c-card c-card--flush")
                articles = [ar for ar in content if ar.find('span', class_="c-meta__type").text == articles_type]
                for article in articles:
                    article_url_r = article.find('a')
                    article_url_a = urljoin(self.url, article_url_r.get('href'))
                    article_text = self.get_article(articles_type, article_url_a)
                    file_name = self.get_file_name(article_url_r.text)
                    self.create_file(i, file_name, article_text)
            else:
                print(f'\nThe URL returned {req}!')

    def get_file_name(self, full_name: str) -> str:
        f = filter(lambda x: x not in string.punctuation, full_name)
        file_name = ''.join(f).replace(" ", "_")
        return file_name

    def get_article(self, article_type: str, url: str) -> str:
        news_content = ""
        req = requests.get(url)
        if req:
            soup = BeautifulSoup(req.content, 'html.parser')
            news_content = soup.find(*NatureScraper.articles_info[article_type])
            news_content = news_content.text.strip()
        else:
            print(f'\nThe URL returned {req}!')
        return news_content

    def create_file(self, page: int, name: str, text: str) -> None:
        file_name = f"Page_{page}/{name}.txt"
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(text)


def main():
    url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page='
    pages = int(input())
    articles_type = input()
    my_scraper = NatureScraper(url)
    my_scraper.run(articles_type, pages)


if __name__ == "__main__":
    main()

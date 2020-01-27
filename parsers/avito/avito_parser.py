import csv
import random
import re
import requests
import time
from collections import namedtuple

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from .invalid import InvalidGetHTML
from .invalid import InvalidGetSoup
from .invalid import InvalidHasNextPage
from .invalid import InvalidGetLinksList


class AvitoParser:
    def __init__(self, page, location, search_query):
        self.page = page
        self.location = location
        self.search_query = search_query

    def create_keywords(self):
        keywords = {
            'page': self.page,
            'location': self.location,
            'search_query': self.search_query
        }

        return keywords

    @staticmethod
    def get_desktop_html(url) -> str:
        header = {
            'authority': 'www.avito.ru',
            'method': 'GET',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
            'cache-control': 'max-age=0',
            'dnt': '1',
            'referer': url,
            'upgrade-insecure-requests': '1',
            'user-agent': UserAgent().random,
        }

        time.sleep(random(1, 2))

        try:
            return requests.get(url, headers=header).text
        except InvalidGetHTML:
            print(f"Error getting HTML code of the page: {url}")
            time.sleep(60)

    @staticmethod
    def get_mobile_html(url) -> str:
        header = {
            'authority': 'm.avito.ru',
            'method': 'GET',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
            'cache-control': 'max-age=0',
            'dnt': '1',
            'referer': url,
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        }

        time.sleep(random(1, 2))

        try:
            return requests.get(url, headers=header).text
        except InvalidGetHTML:
            print(f"Error getting HTML code of the page: {url}")
            time.sleep(60)

    @staticmethod
    def get_soup(html):
        try:
            return BeautifulSoup(html, 'lxml')
        except InvalidGetSoup as ex:
            print(f"Error getting soup of the html")

    @staticmethod
    def has_next_page(soup):
        try:
            if soup.find('a', {'class': 'pagination-page js-pagination-next'}):
                return True
            else:
                return False
        except InvalidHasNextPage:
            print(f"Error in finding next page with soup: {soup}")

    @staticmethod
    def get_links_list(soup):
        try:
            return list(map(lambda s: 'https://www.avito.ru/' + s.get('href'),
                            soup.find_all('a', {'class': 'item-description-title-link'})))
        except InvalidGetLinksList:
            print(f"Error getting list of links with soup: {soup}")

    def get_data_from_link(self):
        pass

    def get_address(self):
        pass

    def get_price(self):
        pass

    def get_phone_number(self):
        pass

    def get_links_from_csv(self):
        pass

    def write_data_to_csv(self):
        pass


def main():
    pass


if __name__ == '__main__':
    pass
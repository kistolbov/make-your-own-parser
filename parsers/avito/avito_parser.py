import csv
import random
import re
import requests
import time
from collections import namedtuple

from bs4 import BeautifulSoup
from fake_useragent import UserAgent


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

    def get_desktop_html(self):
        pass

    def get_mobile_html(self):
        pass

    def get_soup(self):
        pass

    def get_link(self):
        pass

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
import csv
import requests
import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from parsers.hh.invalid import InvalidStatusCode


class HeadHunterParser:
    def __init__(self):
        self.base_url = 'https://ekaterinburg.hh.ru/search/vacancy?area=3&search_period=3&text=python&page=0'
        self.headers = {
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }

    def get_data(self):
        jobs = []
        session = requests.Session()
        request = session.get(self.base_url, headers=self.headers)
        soup = BeautifulSoup(request.content, 'html.parser')
        if request.status_code == 200:
            print(200)
            divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
            for div in divs:
                title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                jobs.append(title)
            print(jobs)
        else:
            raise InvalidStatusCode(f"Invalid status code: {requests.status_codes}")


def main():
    parser = HeadHunterParser()
    parser.get_data()


if __name__ == '__main__':
    main()
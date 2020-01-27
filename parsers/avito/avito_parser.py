import csv
import re
import requests
import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from .invalid import InvalidGetHTML
from .invalid import InvalidGetSoup
from .invalid import InvalidHasNextPage
from .invalid import InvalidGetLinksList
from .invalid import InvalidGetDataFromLink
from .invalid import InvalidGetPrice
from .invalid import InvalidGetAddress
from .invalid import InvalidGetPhoneNumber
from .invalid import InvalidGetLinksFromCSV
from .invalid import InvalidDataUpdate


class AvitoParser:
    def __init__(self, page, location, search_query):
        self.page = page
        self.location = location
        self.search_query = search_query

    def create_keywords(self):
        return {
            'page': str(self.page),
            'location': str(self.location),
            'search_query': str(self.search_query)
        }

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

        time.sleep(2)

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

        time.sleep(2)

        try:
            return requests.get(url, headers=header).text
        except InvalidGetHTML:
            print(f"Error getting HTML code of the page: {url}")
            time.sleep(60)

    @staticmethod
    def get_soup(html):
        try:
            return BeautifulSoup(html, 'lxml')
        except InvalidGetSoup:
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

    @staticmethod
    def get_address(soup):
        try:
            first_address = soup.find('span', {'itemprop': 'name'}).text.strip()
            second_address = soup.find('span', {'class': 'item-map-address'}).text.strip()
            return ', '.join((first_address, second_address))
        except InvalidGetAddress:
            return ' '

    @staticmethod
    def get_price(price):
        try:
            return ' '.join(re.findall(r'\d+', price))
        except InvalidGetPrice:
            return ' '

    @staticmethod
    def get_phone_number(self):
        try:
            return ' '.join(re.findall(r'\d+', soup.find('a', {'href': re.compile('tel:')}).get('href')))
        except InvalidGetPhoneNumber:
            return ' '

    @staticmethod
    def get_data_from_link(soup):
        try:
            name = soup.find('span', {'class': 'title-info-title-text'}).text.strip()
        except InvalidGetDataFromLink:
            name = ' '

        try:
            price = get_price(soup.find('span', {'class': 'js-item-price'}).text.strip())
        except InvalidGetDataFromLink:
            price = ' '

        try:
            seller = soup.find('div', {'class': 'seller-info-name js-seller-info-name'}).find('a').text.strip()
        except InvalidGetDataFromLink:
            seller = ' '

        try:
            address = get_address(soup.find('div', {'class': 'item-map-location'}))
        except InvalidGetDataFromLink:
            address = ' '

        try:
            description = soup.find('div', {'class': 'item-description-text'}).find('p').text.strip()
        except InvalidGetDataFromLink:
            description = ' '

        return {
            'name': name,
            'price': price,
            'seller': seller,
            'address': address,
            'description': description,
        }

    @staticmethod
    def get_links_from_csv(file):
        data = list()

        columns = (
            'name',
            'price',
            'seller',
            'phone_number',
            'link',
            'address',
            'description',
        )

        try:
            with open(file) as file:
                try:
                    reader = csv.DictReader(file, fieldnames=columns)
                    for row in reader:
                        data.append(row.get('link'))
                finally:
                    return data
        except InvalidGetLinksFromCSV:
            return data

    @staticmethod
    def write_data_to_csv(file, data):
        columns = (
            'name',
            'price',
            'seller',
            'phone_number',
            'link',
            'address',
            'description',
        )

        with open(file, 'a') as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writerow(data)


def main():
    parser = AvitoParser('1', 'ekaterinburg', 'lenovo')
    KEYWORDS = parser.create_keywords()
    file = 'avito.csv'

    url = f"https://www.avito.ru/" \
          f"{KEYWORDS.get(location)}?" \
          f"p={KEYWORDS.get(page)}&bt=1&" \
          f"q={KEYWORDS.get(search_query)}"

    links_list = get_links_from_csv(file)

    while has_next_page(get_soup(get_html(url))):
        url = f"https://www.avito.ru/" \
              f"{KEYWORDS.get(location)}?" \
              f"p={KEYWORDS.get(page)}&bt=1&" \
              f"q={KEYWORDS.get(search_query)}"

        KEYWORDS['page'] += 1

        links_list = get_links_list(get_soup(get_html(url)))

        if links_list:
            for link in links_list:
                if link not in visited_links_list:
                    data = dict()
                    try:
                        data.update(get_data_from_link(get_soup(get_html(link))))
                        data['link'] = link
                        data['phone_number'] = get_phone_number(get_soup(get_mobile_html(link)))
                    except InvalidDataUpdate:
                        continue

                    if data['phone_number']:
                        print(f'{len(visited_links_list) + 1}: {data.get("name")}\t{data.get("link")}')
                        write_data_to_csv_file(file, data)
                        visited_links_list.append(link)


if __name__ == '__main__':
    main()
import csv
import requests

from bs4 import BeautifulSoup

from parsers.hh.invalid import InvalidStatusCode


class HeadHunterParser:
    def __init__(self):
        self.base_url = 'https://ekaterinburg.hh.ru/search/vacancy?area=3&search_period=3&text=data+science&page=0'
        self.headers = {
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }

    def get_data(self):
        jobs = []
        urls = [self.base_url]
        session = requests.Session()
        request = session.get(self.base_url, headers=self.headers)
        soup = BeautifulSoup(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            page_quantity = int(pagination[-1].text)
            for i in range(page_quantity):
                url = f"https://ekaterinburg.hh.ru/search/vacancy?area=3&search_period=3&text=python&page={i}"
                if url not in urls:
                    urls.append(url)
        except IndexError:
            pass
        if request.status_code == 200:
            for url in urls:
                request = session.get(url, headers=self.headers)
                soup = BeautifulSoup(request.content, 'lxml')
                divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
                for div in divs:
                    title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                    href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                    company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                    first_text = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                    second_text = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                    content = f"{first_text} {second_text}"
                    jobs.append({
                        'title': title,
                        'href': href,
                        'company': company,
                        'content': content
                    })

            return jobs
        else:
            raise InvalidStatusCode(f"Invalid status code: {requests.status_codes}")

    @staticmethod
    def write_data_to_csv(jobs):
        with open('headhunter.csv', 'a') as file:
            pen = csv.writer(file)
            pen.writerow(('title', 'url', 'company', 'description'))
            for job in jobs:
                pen.writerow((job['title'], job['href'], job['company'], job['content']))


def main():
    parser = HeadHunterParser()
    jobs = parser.get_data()
    parser.write_data_to_csv(jobs)


if __name__ == '__main__':
    main()

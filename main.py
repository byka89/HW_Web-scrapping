import requests
from bs4 import BeautifulSoup as bs
import time
from tqdm import tqdm
import json

URL = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page=0&hhtmFrom=vacancy_search_list"

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'
}


def get_request(url):
    req_html = requests.get(url, headers=HEADERS)
    soup = bs(req_html.text, 'lxml')
    return soup


def get_content(html):
    all_info = html.find("div", class_="vacancy-serp-content")
    message = all_info.find_all("div", class_="serp-item")
    for value in tqdm(message):
        time.sleep(0.1)
        info_link = value.find('a', class_="serp-item__title").get("href")
        if value.find('span', class_="bloko-header-section-3") is None:
            info_salary = "Не указана"
        else:
            info_salary = value.find('span', class_="bloko-header-section-3").text
        company_title = value.find('div', class_="bloko-text").text

        title_city = value.find(attrs={'class': 'bloko-text',
                                       'data-qa': 'vacancy-serp__vacancy-address'}).text
        stick = value.find("div", class_="g-user-content").text
        for search in KEYWORDS:
            if search in stick:
                """ССЫЛКА / ВИЛКА З/П / КОМПАНИЯ / ГОРОД"""
                value_html.append(
                    {
                        "link": info_link,
                        "salary": info_salary,
                        "company": company_title,
                        "city": title_city
                    }
                )
            break


def get_json(list_dict):
    with open("result.json", "w", encoding='utf-8') as outfile:
        json.dump(list_dict, outfile, ensure_ascii=False)


def main():
    result = get_request(f"{URL}")
    last_page = int(result.find_all("span", class_="pager-item-not-in-short-range")[-1].text)
    for page in range(last_page):
        time.sleep(0.3)
        url_1 = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page='
        url_2 = str(page)
        url_3 = '&hhtmFrom=vacancy_search_list'
        result_page = get_request(f"{url_1+url_2+url_3}")
        get_content(result_page)
    print("Запись в JSON")
    get_json(value_html)


if __name__ == '__main__':
    KEYWORDS = ["Django", "Flask"]
    value_html = []
    main()
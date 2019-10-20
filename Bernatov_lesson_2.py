from bs4 import BeautifulSoup as bs
import requests
import time
from pprint import pprint

a = 'https://hh.ru/search/vacancy?area=1&clusters=true&enable_snippets=true&search_field=name&text='
main_link = ('https://hh.ru/search/vacancy?area=1&st=searchVacancy&text=')
search_vacancy = 'Программист'
n = 5
vacancys = {}
for page_number in range(n):
    html = requests.get(f'{main_link}{search_vacancy}&page={page_number}',
                        headers={
                            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}).text
    parsed_html = bs(html, 'lxml')
    block_vac = parsed_html.find('div', {'class': 'vacancy-serp'})
    vacancy_list = block_vac.findChildren(recursive=False)

    vacancys['hh'] = []
    for vacancy in vacancy_list:
        try:
            vacancy_data = {}
            main_info = vacancy.find('span', {'class': 'g-user-content'}).findChild()
            vacancy_name = main_info.getText()
            vacancy_link = main_info['href']
            vacancy_salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).findChild().getText().split()
            if vacancy_salary[0] == 'от':
                vacancy_salary_min = int(vacancy_salary[1]) * 1000
                vacancy_salary_max = ' нет данных'
            elif vacancy_salary[0] == 'до':
                vacancy_salary_min = ' нет данных'
                vacancy_salary_max = int(vacancy_salary[1]) * 1000
            else:
                vacancy_salary_min = int(vacancy_salary[0]) * 1000
                vacancy_salary = vacancy_salary[1].split('-')
                vacancy_salary_max = int(vacancy_salary[1]) * 1000
            vacancy_data['name_vacancy'] = vacancy_name
            vacancy_data['link_vacancy'] = vacancy_link
            vacancy_data['salary_min'] = vacancy_salary_min
            vacancy_data['salary_max'] = vacancy_salary_max
        except AttributeError:
            pass
        vacancys['hh'].append(vacancy_data)
    time.sleep(60)
    # vacancys['job'] = [] ---> здесь должен быть код, который парсит Job.ru но я к сожалению не успел это сделать надеюсь доделать ДЗ в будущем
print(vacancys)

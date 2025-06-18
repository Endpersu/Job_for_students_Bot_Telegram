import requests
import json


def get_vacancies_by_profession(profession):
    params = {
        'text': profession,
        'area': 1,
        'per_page': 5,
        'page': 0,
        'order_by': 'salary_desc'
    }

    response = requests.get('https://api.hh.ru/vacancies',  params=params)

    if response.status_code == 200:
        data = response.json()
        filename = f'hh_vacancies.json'

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return True
    else:
        return False
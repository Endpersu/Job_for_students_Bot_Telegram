import requests
import json


def get_vacancies_by_profession(profession):
    params = {
        'text': profession,        # Профессия, которую ввел пользователь
        'area': 1,                 # Регион (1 - Москва, 2 - СПб)
        'per_page': 5,            # Количество вакансий (макс. 100)
        'page': 0,                 # Номер страницы
        'order_by': 'salary_desc'  # Сортировка по убыванию зарплаты
    }

    response = requests.get('https://api.hh.ru/vacancies', params=params)

    if response.status_code == 200:
        data = response.json()
        filename = f'hh_vacancies.json'

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Найдено {data['found']} вакансий по профессии '{profession}'")
        print(f"Данные сохранены в файл '{filename}'")
    else:
        print(f"Ошибка {response.status_code}: {response.text}")

a = input("профессия: ")
get_vacancies_by_profession(a)

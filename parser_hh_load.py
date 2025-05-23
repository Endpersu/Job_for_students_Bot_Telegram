import json

with open("hh_vacancies.json", 'r', encoding='utf-8') as file_vacancies:
    data = json.load(file_vacancies)

for item in data['items']:
    vacancy_name = item['name']
    city_name = item['area']['name']
    alternate_url = item['alternate_url']
    money_1 = item['salary']['from']
    money_2 = item['salary']['to']
    requirement = item['snippet']['requirement']
    responsibility = item['snippet']['responsibility']

    if money_1 and money_2:
        salary_str = f"{money_1} – {money_2}"
    elif money_1:
        salary_str = f"от {money_1}"
    elif money_2:
        salary_str = f"до {money_2}"
    else:
        salary_str = "Не указана"

    print(f"Вакансия: {vacancy_name}")
    print(f"Город: {city_name}")
    print(f"Ссылка на вакансию: {alternate_url}")
    print(f"Требования: {requirement}")
    print(f"Обязанности: {responsibility}")
    print(f"Зарплата: {salary_str}")

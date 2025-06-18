import json


def load_vacancies():
    try:
        with open("hh_vacancies.json", 'r', encoding='utf-8') as file_vacancies:
            data = json.load(file_vacancies)

        vacancies = []
        for item in data['items']:
            vacancy_name = item['name']
            city_name = item['area']['name']
            alternate_url = item['alternate_url']
            money_1 = item['salary']['from'] if item['salary'] and 'from' in item['salary'] else None
            money_2 = item['salary']['to'] if item['salary'] and 'to' in item['salary'] else None
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

            vacancies.append({
                'name': vacancy_name,
                'city': city_name,
                'url': alternate_url,
                'salary': salary_str,
                'requirement': requirement,
                'responsibility': responsibility
            })

        return vacancies

    except FileNotFoundError:
        return None
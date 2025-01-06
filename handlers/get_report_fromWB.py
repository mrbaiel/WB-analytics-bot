from http.client import responses

import requests


def get_sales_report(api_key, date_from, end_date):
    url = 'https://statistics-api.wildberries.ru/api/v1/supplier/sales'
    headers = {'Authorization': f'{api_key}'}
    params = {
        'dateFrom': date_from,
        'dateTo': end_date
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        raise Exception(f"Ошибка API {response.status_code}, {response.text}")
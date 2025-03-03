import json
import requests

def get_erir_statuses_data(api_token=None, data_type='creative', offset=0, limit=10, limit_per_entity=10, external_ids=None):
    """
    Выполняет запрос к API для получения статусов ЕРИР и извлекает значение 'erir_status'.

    Args:
        api_token (str): Токен авторизации API Bearer.
        data_type (str, optional): Тип данных для запроса (creative, contract, etc.). Defaults to 'creative'.
        offset (int, optional): Смещение для пагинации. Defaults to 0.
        limit (int, optional): Количество результатов на странице. Defaults to 10.
        limit_per_entity (int, optional): Лимит на сущность. Defaults to 1.
        external_ids (list, optional): Список external_id для фильтрации. Defaults to None.

    Returns:
        str or None: Значение 'erir_status' в случае успешного запроса и наличия,
                     None в случае ошибки, отсутствия данных или если 'erir_status' не найден.
                     В случае ошибки также выводит сообщение об ошибке в консоль.
    """
    url = 'https://api.ord.vk.com/v1/erir_statuses'

    params = {
        'data_type': data_type,
        'offset': offset,
        'limit': limit,
        'limit_per_entity': limit_per_entity,
    }
    if external_ids:
        params['external_id'] = external_ids

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json() # Декодируем JSON ответ
        items = data.get("items") # Получаем список items

        if items and isinstance(items, list) and len(items) > 0: # Проверяем, что items не пустой список
            first_item = items[0] # Берем первый элемент списка items
            erir_status = first_item.get("erir_status") # Пытаемся получить значение 'erir_status'
            if erir_status:
                return erir_status # Возвращаем значение 'erir_status'
            else:
                print("Предупреждение: Ключ 'erir_status' не найден в элементе items.")
                return None # Возвращаем None, если 'erir_status' не найден
        else:
            print("Предупреждение: Ключ 'items' не найден, items не является списком или пуст.")
            return None # Возвращаем None, если структура JSON не соответствует ожидаемой

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text: {response.text}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return None
    except json.JSONDecodeError as json_err:
        print(f"JSON decode error occurred: {json_err}")
        print(f"Response text: {response.text}")
        return None

def get_creative_list_data(api_token, limit=5, offset=0):
    """
    Выполняет запрос к API для получения списка креативов (erid и external_id).

    Args:
        api_token (str): Токен авторизации API Bearer.
        limit (int, optional): Количество результатов на странице. Defaults to 5.
        offset (int, optional): Смещение для пагинации. Defaults to 0.

    Returns:
        list or None: Список словарей с 'erid' и 'external_id' в случае успеха,
                      None в случае ошибки или отсутствия данных.
                      В случае ошибки также выводит сообщение об ошибке в консоль.
    """
    url = 'https://api.ord.vk.com/v1/creative/list/erid_external_ids'

    params = {
        'limit': limit,
        'offset': offset,
    }

    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Вызывает исключение для кодов ошибок 4xx и 5xx
        data = response.json()      # Декодируем JSON ответ
        items = data.get("items")    # Получаем список items из ответа

        if items and isinstance(items, list): # Проверяем, что items - это список и не пустой
            creative_list = []
            for item in items:
                erid = item.get("erid")
                external_id = item.get("external_id")
                if erid and external_id: # Проверяем, что erid и external_id присутствуют в элементе
                    creative_list.append({"erid": erid, "external_id": external_id})
            return creative_list # Возвращаем список словарей

        else:
            print("Предупреждение: Ключ 'items' не найден или items не является списком.")
            return None # Возвращаем None, если структура JSON не соответствует ожидаемой

    except requests.exceptions.HTTPError as http_err:
        print(f"Ошибка HTTP запроса: {http_err}")
        print(f"Текст ответа: {response.text}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Ошибка запроса: {req_err}")
        return None
    except json.JSONDecodeError as json_err:
        print(f"Ошибка декодирования JSON: {json_err}")
        print(f"Текст ответа: {response.text}")
        return None

def get_last_5_creative_statuses_string(api_token):
    """
    Возвращает строку с информацией о статусах ЕРИР для последних 5 креативов.

    Args:
        api_token (str): Токен авторизации API Bearer.

    Returns:
        str: Строка, содержащая информацию о последних 5 парах "токен + статус ЕРИР".
             В случае ошибки или отсутствия данных возвращает информационное сообщение об ошибке.
    """
    creative_list = get_creative_list_data(api_token=api_token, limit=5)
    if not creative_list:
        return "Ошибка при получении списка креативов или список креативов пуст."

    result_string_lines = ["Последние 5 креативов и их статусы ЕРИР:\n"]

    for creative_item in creative_list:
        external_id = creative_item['external_id']
        erir_status = get_erir_statuses_data(api_token=api_token, external_ids=[external_id]) # Передаем external_id как список

        if erir_status:
            result_string_lines.append(f"Токен: {creative_item['erid']}, Статус ЕРИР: {erir_status}")
        else:
            result_string_lines.append(f"Токен: {creative_item['erid']}, Статус ЕРИР: Не удалось получить статус") # Сообщение, если статус не получен

    return "\n".join(result_string_lines) # Соединяем строки в одну с переносом строк
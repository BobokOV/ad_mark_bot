import asyncio

from aiohttp import ClientSession
import datetime

from config.api_token import API_TOKEN


def is_date_relevant(date_string: str):
    try:
        date_object = datetime.datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        current_datetime = datetime.datetime.now(datetime.timezone.utc)
        time_difference = current_datetime - date_object
        three_days = datetime.timedelta(days=4)
        return time_difference <= three_days
    except ValueError:
        print("Ошибка: Неверный формат строки даты.")
        return False

def process_data_to_strings(data):
    grouped_data = {}
    output_string = ""

    for item in data:
        name, status, item_type, date_str = item
        date_obj = datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00'))

        if item_type not in grouped_data:
            grouped_data[item_type] = []
        grouped_data[item_type].append({'name': name, 'status': status, 'type': item_type, 'date': date_obj, 'original_date_str': date_str})

    for item_type in grouped_data:
        grouped_data[item_type].sort(key=lambda x: x['date'])

        type_string = f"Тип: {item_type}\n"
        for item in grouped_data[item_type]:
            type_string += f"    Имя: {item['name']}, Статус: {item['status']}\n" # Добавляем информацию об элементе
        output_string += type_string

    return output_string


class HTTPClient:
    def __init__(self, base_url: str, api_token: str):
        self._base_url = base_url
        self._headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'accept': 'application/json'
        }
        self._session = None  # Инициализируем _session как None в __init__

    async def __aenter__(self):  # Асинхронный метод для входа в контекст
        self._session = ClientSession(  # Создаем сессию при входе в контекст
            base_url=self._base_url,
            headers=self._headers
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):  # Асинхронный метод для выхода из контекста
        if self._session:  # Проверяем, что сессия была создана
            await self._session.close()  # Закрываем сессию при выходе из контекста

    @property
    def session(self):  # Добавим property для доступа к сессии внутри контекста
        if not self._session:
            raise RuntimeError("Client session is not initialized. Use within 'async with' context.")
        return self._session


class ORDHTTPClient(HTTPClient):
    # Тут получим статусы публикаций
    async def __get_erir_statuses(self):
        async with self.session.get("/v1/erir_statuses") as resp:
            return await resp.json()

    # Тут получим список креативов
    async def __get_creatives(self, limit=1000, offset=0):
        async with self.session.get("/v1/creative",
                                    params={
                                        'limit': limit,
                                        'offset': offset}
                                    ) as resp:
            result = await resp.json()
            return result

    # Отсюда получим eid договора
    async def __get_creative(self, eid: str):
        async with self.session.get(f"/v2/creative/{eid}") as resp:
            result = await resp.json()
            return result

    # Отсюда получим eid контрагента
    async def __get_contract(self, eid: str):
        async with self.session.get(f"/v1/contract/{eid}") as resp:
            result = await resp.json()
            return result

    # Отсюда получим ФИО
    async def __get_person(self, eid: str):
        async with self.session.get(f"/v1/person/{eid}") as resp:
            result = await resp.json()
            return result

    # Отсюда получим список рекламных площадок
    async def __get_pads(self, limit=1000, offset=0):
        async with self.session.get("/v1/pad",
                                    params={
                                        'limit': limit,
                                        'offset': offset}
                                    ) as resp:
            result = await resp.json()
            return result

    # Отсюда получим данные рекламной площадки (eid контрагента и url)
    async def __get_pad(self, eid: str):
        async with self.session.get(f"/v1/pad/{eid}") as resp:
            result = await resp.json()
            return result

    async def get_erid_statuses(self):
        try:
            result = await self.__get_erir_statuses()
            items = result['items']
            bad_or_processing = [
                {'data_type': item['data_type'],
                 'external_id': item['external_id'],
                 'updated_by_user_ts': item['updated_by_user_ts'],
                 'erir_status': item['erir_status']
                 } for item in items]

            erir_statuses = []

            for item in bad_or_processing:
                if not is_date_relevant(item['updated_by_user_ts']):
                    continue
                data_type = item['data_type']
                if data_type == 'person':
                    stat = await self.__get_person(item['external_id'])
                    name = stat['name']
                elif data_type == 'contract':
                    stat = await self.__get_contract(item['external_id'])
                    name = stat['comment']
                elif data_type == 'creative':
                    stat = await self.__get_creative(item['external_id'])
                    name = stat['erid']
                elif data_type == 'pad':
                    stat = await self.__get_pad(item['external_id'])
                    name = stat['name']
                else:
                    name = ''

                erir_statuses.append([name, item['erir_status'], item['data_type'], item['updated_by_user_ts']])

            return process_data_to_strings(erir_statuses)
        except Exception as e:
            return f"Ошибка: {e}"

async def main():
    async with ORDHTTPClient(base_url="https://api.ord.vk.com",
                             api_token=API_TOKEN) as ord_client:
        text = await ord_client.get_erid_statuses()
        print(text)

if __name__ == "__main__":
    asyncio.run(main())
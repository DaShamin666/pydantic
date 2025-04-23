from pydantic import BaseModel,HttpUrl
from typing import List
import requests


class PageModel(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int

class DataModel(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: HttpUrl

class SupportModel(BaseModel):
    url: HttpUrl
    text: str

class ResponseModel(BaseModel):
    page: PageModel
    data: List[DataModel]
    support: SupportModel

def test_users_pagination():
    response = requests.get('https://reqres.in/api/users?page=1')
    assert response.status_code == 200
    response_json = response.json()


    page_data = PageModel(**{key: response_json[key] for key in ['page', 'per_page', 'total', 'total_pages']})

    response_data = ResponseModel(page=page_data, data=response_json['data'], support=response_json['support'])

    assert len(response_data.data) == response_data.page.per_page, 'Количество пользователей не совпадает с per_page'
    assert response_data.page.page > 0, 'Текущая страница должна быть больше 0'
    assert response_data.page.per_page > 0, 'Количество элементов на странице должно быть больше 0'
    assert response_data.page.total >= len(
        response_data.data), 'Общее количество элементов должно быть больше или равно количеству полученных данных'
    assert response_data.page.total_pages > 0, 'Общее количество страниц должно быть больше 0'

    print('Все проверки пройдены успешно!')


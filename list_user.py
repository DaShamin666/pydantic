from pydantic import BaseModel,HttpUrl
from typing import List
import requests


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
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[DataModel]
    support: SupportModel


def test_users_pagination():
    response = requests.get('https://reqres.in/api/users?page=1')
    assert response.status_code == 200

    response_data = ResponseModel(**response.json())

    assert len(response_data.data) == response_data.per_page, 'Количество пользователей не совпадает с per_page'
    assert response_data.page > 0, 'Текущая страница должна быть больше 0'
    assert response_data.per_page > 0, 'Количество элементов на странице должно быть больше 0'
    assert response_data.total >= len(
        response_data.data), 'Общее количество элементов должно быть больше или равно количеству полученных данных'
    assert response_data.total_pages > 0, 'Общее количество страниц должно быть больше 0'

    print('Все проверки пройдены успешно!')

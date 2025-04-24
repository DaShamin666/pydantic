from pydantic import BaseModel,HttpUrl
import requests

class Model(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: HttpUrl

class SupportModel(BaseModel):
    url: HttpUrl
    text: str

class ResponseModel(BaseModel):
    support: SupportModel
    data: Model


def test_user():
    response = requests.get('https://reqres.in/api/users/1')
    assert response.status_code == 200
    user_data = ResponseModel(**response.json())
    assert user_data.data.id == 1
    print(user_data)



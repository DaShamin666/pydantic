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
    assert isinstance(response.json()['data']['email'], str)
    assert isinstance(response.json()['data']['first_name'], str)
    assert isinstance(response.json()['data']['last_name'], str)
    assert isinstance(response.json()['data']['avatar'], str)
    assert response.json()["data"]['id'] == 1
    print(ResponseModel(**response.json()))



new_user = Model(
    id=666,
    email="fjdkjfk@mail.com",
    first_name="Xui",
    last_name="Bolshie",
    avatar="https://zefirka.club/uploads/posts/2022-10/1664852614_2-zefirka-club-p-avatarki-s-billi-gachi-2.jpg"
)


support_info = SupportModel(
    url="https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral",
    text="Ura Tovarishi"
)

response_model = ResponseModel(
    support=support_info,
    data=new_user
)

print(response_model)
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional
import requests
from faker import Faker
from datetime import datetime

fake = Faker()

class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    job: Optional[str] = None

    @field_validator('name')
    def validate_name(cls, value):
        if value is not None:
            if not isinstance(value, str):
                raise ValidationError('Имя должно быть строкой')
            if len(value) < 2 or len(value) > 50:
                raise ValidationError('Имя должно быть от 2 до 50 символов')
            if not value.replace(' ', '').isalpha():
                raise ValidationError('Имя должно содержать только буквы и пробелы')
        return value

    @field_validator('job')
    def validate_job(cls, value):
        if value is not None:
            if not isinstance(value, str):
                raise ValidationError('Название работы должно быть строкой')
            if len(value) < 2 or len(value) > 100:
                raise ValidationError('Название работы должно быть от 2 до 100 символов')
            if not value.replace(' ', '').isalnum():
                raise ValidationError('Название работы должно содержать только буквы, цифры и пробелы')
        return value

class UpdateUserResponse(BaseModel):
    name: str
    job: str
    updatedAt: datetime = Field(default_factory=datetime.now)

    @field_validator('name')
    def validate_name(cls, value):
        if len(value) < 2 or len(value) > 50:
            raise ValidationError('Имя должно быть от 2 до 50 символов')
        if not value.replace(' ', '').isalpha():
            raise ValidationError('Имя должно содержать только буквы и пробелы')
        return value

    @field_validator('job')
    def validate_job(cls, value):
        if len(value) < 2 or len(value) > 100:
            raise ValidationError('Название работы должно быть от 2 до 100 символов')
        if not value.replace(' ', '').isalnum():
            raise ValidationError('Название работы должно содержать только буквы, цифры и пробелы')
        return value

    @field_validator('updatedAt')
    def validate_updated_at(cls, value):
        if not isinstance(value, datetime):
            raise ValidationError('Дата обновления должна быть объектом datetime')
        return value


def test_update_user():
    new_user_update = UpdateUserRequest(
        name=fake.name(),
        job=fake.job()
    )
    response = requests.patch(url='https://reqres.in/api/users/2', json=new_user_update.model_dump())
    assert response.status_code == 200
    response_data = UpdateUserResponse(**response.json())
    assert response_data.name == new_user_update.name
    assert response_data.job == new_user_update.job
    assert response_data.updatedAt is not None
    assert isinstance(response_data.updatedAt, datetime)
    print('Пользователь успешно обновлен')




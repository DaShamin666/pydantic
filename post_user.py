from pydantic import BaseModel, Field, field_validator, ValidationError
import requests
from faker import Faker
from datetime import datetime

fake = Faker()

class UserRequest(BaseModel):
    name: str
    job: str

    @field_validator('name')
    def validate_name_length(cls, value):
        if len(value) < 2 or len(value) > 50:
            raise ValidationError('Имя должно быть от 2 до 50 символов')
        return value

    @field_validator('job')
    def validate_job_length(cls, value):
        if len(value) < 2 or len(value) > 100:
            raise ValidationError('Название работы должно быть от 2 до 100 символов')
        return value


class UserResponse(BaseModel):
    name: str
    job: str
    id: str
    createdAt: datetime = Field(default_factory=datetime.now)

    @field_validator('name')
    def validate_name_length(cls, value):
        if len(value) < 2 or len(value) > 50:
            raise ValidationError('Имя должно быть от 2 до 50 символов')
        return value

    @field_validator('job')
    def validate_job_length(cls, value):
        if len(value) < 2 or len(value) > 100:
            raise ValidationError('Название работы должно быть от 2 до 100 символов')
        return value

    @field_validator('id')
    def validate_id(cls, value):
        if not value:
            raise ValidationError('ID не может быть пустым')
        return value

    @field_validator('createdAt')
    def validate_created_at(cls, value):
        if not value:
            raise ValidationError('Дата создания не может быть пустой')
        return value


def test_create_user():
    data = {
        "name": fake.name(),
        "job": fake.job(),
    }
    user = UserRequest(**data)
    response = requests.post('https://reqres.in/api/users', json=user.model_dump())
    assert response.status_code == 201
    response_data = UserResponse(**response.json())
    assert response_data.id is not None
    assert response_data.name == user.name
    assert response_data.job == user.job
    assert response_data.createdAt is not None
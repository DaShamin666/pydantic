from pydantic import BaseModel, Field, field_validator, ValidationError
import requests
from faker import Faker
from datetime import datetime

fake = Faker()

class UserRequest(BaseModel):
    name: str
    job: str


class UserResponse(BaseModel):
    name: str
    job: str
    id: str
    createdAt: datetime = Field(default_factory=datetime.now)

    @classmethod
    @field_validator('name', 'job', 'id', 'createdAt')
    def validate_fields(cls, value, field):
        if not value:
            raise ValidationError(f'Invalid value for {field.name}: must not be empty')
        return value



def test_create_user():
    data = {
        "name": fake.name(),
        "job": fake.job(),
    }
    user =UserRequest(**data)
    response = requests.post('https://reqres.in/api/users', json=user.dict())
    assert response.status_code == 201
    response_data = UserResponse(**response.json())
    assert response_data.id is not None
    assert response_data.name == user.name
    assert response_data.job == user.job
    assert response_data.createdAt is not None

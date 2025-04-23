from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional
import requests
from faker import Faker
from datetime import datetime

fake = Faker()

class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    job: Optional[str] = None

    @classmethod
    @field_validator('name', 'job')
    def validate_fields(cls, value, field):
        if value is not None and not isinstance(value, str):
            raise ValidationError(f'Invalid type for {field.name}: must be a string')
        if value == "":
            raise ValidationError(f'Invalid value for {field.name}: must not be empty')
        return value

class UpdateUserResponse(BaseModel):
    name: str
    job: str
    updatedAt: datetime = Field(default_factory=datetime.now)


def test_update_user():
    new_user_update = UpdateUserRequest(
        name=fake.name(),
        job=fake.job()
    )
    response = requests.patch(url='https://reqres.in/api/users/2', json=new_user_update.dict())
    assert response.status_code == 200
    response_data = UpdateUserResponse(**response.json())
    assert response_data.name == new_user_update.name
    assert response_data.job == new_user_update.job




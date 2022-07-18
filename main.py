import pytest
import requests
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ValidationError, validator



headers = {
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDIsImV4cCI6MTY2MjcwOTc4NSwiY3JlYXRlZCI6MTY1NzU'
                   'yNTc4NX0.9zZfN7-5ydY10ySOb-iS-oybpPVfnaAznIHocUhxlh8',
  'Content-Type': 'application/json'
}


class ResultStructure(BaseModel):
    pk: int
    author: int
    author_name: str
    comments: int
    created_date: datetime
    text: int
    pic: str
    likes: int
    current_user_rate: int

    @validator('pk')
    def integer_check(cls, pk):
        if not str(pk).isdigit():
            raise ValueError('PK must be integer!!')
        return pk




class Post(BaseModel):
    count: int
    next: str
    previous: Optional[str]
    results: List[ResultStructure]


try:
    response = requests.get('https://meme.gcqadev.ru/api/v2/post_list/')
    parsed = Post.parse_obj(response.json())
except ValidationError as e:
    print(e)



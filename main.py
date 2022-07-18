import pytest
import requests
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ValidationError, validator, Field



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
    text: str
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


class Comments(BaseModel):
    post: int
    comment_id: int
    user: int
    username: int
    date_of_comment: datetime
    text: str
    parent_comment: Optional[int]


try:
    comments = requests.get('https://meme.gcqadev.ru/api/v1/post/70/comments/', headers=headers)
    Comments.parse_obj(comments.json()[0])
except ValidationError as e:
    print(e)


comments = requests.get('https://meme.gcqadev.ru/api/v1/post/70/comments/', headers=headers)
Comments.parse_obj(comments.json()[0])
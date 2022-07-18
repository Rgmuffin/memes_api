import pytest
import requests
import json
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


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
    created_date: str
    text: str
    pic: str
    likes: int
    current_user_rate: int


class Post(BaseModel):
    count: int
    next: str
    previous: Optional[str]
    results: List[ResultStructure]

response = requests.get('https://meme.gcqadev.ru/api/v2/post_list/')
parsed = Post.parse_obj(response.json())
print(parsed)

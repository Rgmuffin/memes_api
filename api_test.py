import pytest
import requests
import json
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
    text: str
    pic: str
    likes: int
    current_user_rate: int

    @validator('pk', 'author', 'comments', 'likes', 'current_user_rate')
    def integer_check(cls, v):
        if not str(v).isdigit():
            raise ValueError('Value must be an integer!')
        return v


class Post(BaseModel):
    count: int
    next: str
    previous: Optional[str]
    results: List[ResultStructure]

    @validator('count')
    def integer_check(cls, count):
        if not str(count).isdigit():
            raise ValueError('PK must be an integer!')
        return count


class Comments(BaseModel):
    post: int
    comment_id: int
    user: int
    username: str
    date_of_comment: datetime
    text: str
    parent_comment: Optional[str]

    @validator('post', 'comment_id', 'user')
    def integer_check(cls, v):
        if not str(v).isdigit():
            raise ValueError('Value must be an integer!')
        return v


def test_post_list():
    try:
        response = requests.get('https://meme.gcqadev.ru/api/v2/post_list/')
        assert response.status_code == 200
        Post.parse_obj(response.json())
    except ValidationError as e:
        raise ValueError(e)


def test_comment_list():
    try:
        comments = requests.get('https://meme.gcqadev.ru/api/v1/post/70/comments/', headers=headers)
        Comments.parse_obj(comments.json()[0])
    except ValidationError as e:
        raise ValueError(e.json())

def test_post_list_by_tag():
    tag = 'family'
    url = 'https://meme.gcqadev.ru/api/v2/post_list/' + tag
    response = requests.get(url)
    assert response.status_code == 200


def test_mark_as_read():
    post_id = '118'
    url = 'https://meme.gcqadev.ru/api/v1/post/' + post_id + '/mark_read/'
    response = requests.post(url, headers=headers)
    assert response.status_code == 201


def test_like():
    post_id = '118'
    url = 'https://meme.gcqadev.ru/api/v1/post/' + post_id + '/like/up/'
    response = requests.post(url, headers=headers)
    if response.text == '["That rate is already exist"]':
        remove_like = requests.delete(url, headers=headers)
        assert remove_like.status_code == 204
        response = requests.post(url, headers=headers)
    assert response.status_code == 201


def test_add_comment():
    post_id = '70'
    url = 'https://meme.gcqadev.ru/api/v1/post/' + post_id + '/comment/'
    payload = json.dumps({"text": "pytest"})
    response = requests.post(url, headers=headers, data=payload)
    assert response.status_code == 201
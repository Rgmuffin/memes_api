import pytest
import requests
import json
from pydantic import BaseModel

headers = {
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDIsImV4cCI6MTY2MjcwOTc4NSwiY3JlYXRlZCI6MTY1NzU'
                   'yNTc4NX0.9zZfN7-5ydY10ySOb-iS-oybpPVfnaAznIHocUhxlh8',
  'Content-Type': 'application/json'
}


class Post(BaseModel):
    pk: int
    author: int
    author_name: str
    comments: int
    created_date: str
    text: str
    pic: str
    likes: int
    current_user_rate: int


def test_post_list():
    response = requests.get('https://meme.gcqadev.ru/api/v2/post_list/')
    assert Post.parse_obj(response.json()['results'][0])


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
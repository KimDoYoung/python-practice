
from unittest import mock

import pytest
import requests
import source.service as service

# 1. patch 함수를 fullpath로 지정
# 2. mocker => mock_함수명
# 3. mocker.return_value = 값
# 4. assert (함수를 실제로 수행하고 결과값은 return_value로 한다)
@mock.patch("source.service.get_user_from_db")
def test_get_user_from_db(mock_get_user_from_db):
    mock_get_user_from_db.return_value = "John"
    assert service.get_user_from_db(1) == "John"


@mock.patch("requests.get")
def test_get_usrs(mock_get):
    response = mock.Mock()
    response.status_code = 200
    response.json.return_value = [{"id": 1, "name": "John"}]    

    mock_get.return_value = response
    assert service.get_users() == [{"id": 1, "name": "John"}]    

@mock.patch("requests.get")
def test_get_usrs_error(mock_get):
    response = mock.Mock()
    response.status_code = 400
    mock_get.return_value = response
    with pytest.raises(requests.HTTPError):
        service.get_users()

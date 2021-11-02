import requests
import pytest
from unittest.mock import Mock, MagicMock, create_autospec
from majortom_scripting import ScriptingAPI
from majortom_scripting.exceptions import QueryError, ScriptDisabledError, RateLimitError, TokenInvalidError

def test_required_args():
    with pytest.raises(TypeError):
        ScriptingAPI()

def test_init_makes_no_api_calls():
  # Any attempted network calls will fail
  ScriptingAPI(host="blah", token="abcdefg")

class MockResponse:
  def __init__(self, status_code) -> None:
      self.status_code = status_code
      self.headers = {
        'x-ratelimit-resetafter': 10,
        'x-ratelimit-retryafter': 20,
      }
  def json():
    return {
      "errors": ["A list of errors"]
    }

def test_disabled_script_generates_correct_error(monkeypatch):
  mock_response = MagicMock(status_code=422)
  mock_post = Mock(return_value=mock_response)
  monkeypatch.setattr(requests, "post", mock_post)

  with pytest.raises(ScriptDisabledError):
    ScriptingAPI("host", "token").script_id()


def test_correct_error_generated_when_rate_limit_status_code_received(monkeypatch):
  methods = {'json.return_value': {
      "errors": ["Ya dun goofed"]
    }}
  mock_response = MagicMock(
    status_code=420,
    headers={
        'x-ratelimit-resetafter': 10,
        'x-ratelimit-retryafter': 20,
      },
    **methods
  )
  mock_post = Mock(return_value=mock_response)
  monkeypatch.setattr(requests, "post", mock_post)

  with pytest.raises(RateLimitError):
    ScriptingAPI("host", "token").script_id()

def test_correct_error_generated_when_token_invalid_status_code_received(monkeypatch):
  mock_response = MagicMock(status_code=403)
  mock_post = Mock(return_value=mock_response)
  monkeypatch.setattr(requests, "post", mock_post)

  with pytest.raises(TokenInvalidError):
    ScriptingAPI("host", "token").script_id()

def test_correct_error_generated_when_server_barfs(monkeypatch):
  fake_response = requests.Response()
  fake_response.status_code = 500
  mock_post = Mock(return_value=fake_response)
  monkeypatch.setattr(requests, "post", mock_post)

  with pytest.raises(requests.exceptions.HTTPError):
    ScriptingAPI("host", "token").script_id()

def test_correct_error_generated_when_server_barfs(monkeypatch):
  mock_response = MagicMock(status_code=200)
  mock_response.json.return_value = {"errors": ["Ya dun goofed"]}
  mock_post = Mock(return_value=mock_response)
  monkeypatch.setattr(requests, "post", mock_post)

  with pytest.raises(QueryError):
    ScriptingAPI("host", "token").script_id()


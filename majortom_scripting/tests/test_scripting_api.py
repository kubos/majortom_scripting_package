import pytest
from majortom_scripting import ScriptingAPI

def test_required_args():
    with pytest.raises(TypeError):
        ScriptingAPI()

def test_init_makes_no_api_calls():
  # Any attempted network calls will fail
  ScriptingAPI(host="blah", token="abcdefg")

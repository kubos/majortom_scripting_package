import pytest
import json
from majortom_scripting.modeling_api import ModelingAPI
from majortom_scripting.models.mission import Mission
from majortom_scripting.models.satellite import Satellite
from majortom_scripting import ModelingAPI, ScriptingAPI
from majortom_scripting.mutations import Mutations
from majortom_scripting.exceptions import PassNotFoundError
from unittest.mock import Mock, ANY, create_autospec, MagicMock

@pytest.fixture()
def pass_result():
  with open('./majortom_scripting/tests/fixtures/passes.json', 'r') as f:
    return json.loads(f.read())

@pytest.fixture()
def cmd_defs_response():
  with open('./majortom_scripting/tests/fixtures/command_defs_response.json', 'r') as f:
    return json.loads(f.read())

def test_init_makes_no_api_calls():
  api_mock = Mock(spec=ModelingAPI)
  Satellite(api_mock, id=1, name="Sat E. Lite")
  assert len(api_mock.mock_calls) == 0, "No calls to the API should happen on init"

def test_passes_property(pass_result):
  api_mock = Mock(spec=ModelingAPI)
  inner_api_mock = create_autospec(ScriptingAPI)
  api_mock.scripting_api = inner_api_mock
  inner_api_mock.system.return_value = pass_result
  
  sat = Satellite(api_mock, id=1, name="Sat E. Lite")
  passes = sat.passes

  inner_api_mock.system.assert_called_once_with(id=1, return_fields=ANY)
  assert len(passes) > 100, "There should be a bunch of pass objects in the array"

  # Make sure that a second access doesn't hit the API again
  sat.passes
  inner_api_mock.system.assert_called_once_with(id=1, return_fields=ANY)

def test_next_pass_method(pass_result):
  api_mock = Mock(spec=ModelingAPI)
  inner_api_mock = create_autospec(ScriptingAPI)
  api_mock.scripting_api = inner_api_mock
  inner_api_mock.system.return_value = pass_result
  
  sat = Satellite(api_mock, id=1, name="Sat E. Lite")
  now = 1633452497914
  next = sat.next_pass(current_unix_time_ms=now)

  assert next
  assert next.start > now
  assert next.id == "2566"

def test_next_pass_method_with_scheduled_passes(pass_result):
  api_mock = Mock(spec=ModelingAPI)
  inner_api_mock = create_autospec(ScriptingAPI)
  api_mock.scripting_api = inner_api_mock
  inner_api_mock.system.return_value = pass_result
  
  sat = Satellite(api_mock, id=1, name="Sat E. Lite")
  now = 1633452497914
  next = sat.next_pass(current_unix_time_ms=now, scheduled=True)

  assert next
  assert next.start > now
  assert next.id == "2568"

def test_next_pass_method_raises_not_found_error_when_no_more_passes_exist(pass_result):
  api_mock = Mock(spec=ModelingAPI)
  inner_api_mock = create_autospec(ScriptingAPI)
  api_mock.scripting_api = inner_api_mock
  inner_api_mock.system.return_value = pass_result
  
  sat = Satellite(api_mock, id=1, name="Sat E. Lite")
  
  with pytest.raises(PassNotFoundError):
    sat.next_pass(current_unix_time_ms=9999999999999)

def test_get_command_definitions(cmd_defs_response):
  api_mock = Mock(spec=ModelingAPI)
  inner_api_mock = create_autospec(ScriptingAPI)
  api_mock.scripting_api = inner_api_mock
  inner_api_mock.command_definitions.return_value = cmd_defs_response
  
  sat = Satellite(api_mock, id=1, name="AQUA")

  defs = sat.command_definitions
  assert len(defs) > 1    # Make sure we get mock results
  inner_api_mock.command_definitions.assert_called()

def test_update_command_definitions():
  # ToDo: Find a better way to test w/o deeply-nested mocks.
  api_mock = Mock(spec=ModelingAPI)
  inner_api_mock = Mock(spec=ScriptingAPI)
  mutations_mock = Mock(spec=Mutations)
  inner_api_mock.mutations = mutations_mock
  api_mock.scripting_api = inner_api_mock
  mutations_mock.update_command_definitions.return_value = {'success': True, 'notice': 'Command definitions updated', 'errors': []}
  
  sat = Satellite(api_mock, id=1, name="AQUA")

  new_defs = '''
    {
    "definitions": {
        "ping": {
        "display_name": "Ping",
        "description": "A simple ping. The Gateway should pretend to contact the satellite and return a pong.",
        "tags": [
            "testing",
            "operations"
        ],
        "fields": []
        }
    }
    }
    '''
  
  sat.update_command_definitions(new_defs)

  mutations_mock.update_command_definitions.assert_called()


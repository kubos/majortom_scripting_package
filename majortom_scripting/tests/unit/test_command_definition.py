import pytest
import json
from majortom_scripting.modeling_api import ModelingAPI
from majortom_scripting.models.mission import Mission
from majortom_scripting.models.command_definition import CommandDefinition
from majortom_scripting import ModelingAPI, ScriptingAPI
from majortom_scripting.mutations import Mutations
from majortom_scripting.exceptions import PassNotFoundError
from unittest.mock import Mock, ANY, create_autospec, MagicMock


def test_conversion_to_json():
  api_mock = Mock(spec=ModelingAPI)
  ping = CommandDefinition(api_mock, id=1, description="Def description", tags=['testing', 'operations'], 
    fields="[]", displayName="Ping", commandType="ping", starred=True)
  assert ping.to_json() == '{"ping": {"fields": [], "description": "Def description", "tags": ["testing", "operations"], "display_name": "Ping"}}'


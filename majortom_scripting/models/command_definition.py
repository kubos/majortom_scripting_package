import json
import copy
import re

def camel_to_snake(name):
  pattern = re.compile(r'(?<!^)(?=[A-Z])')
  return pattern.sub('_', name).lower()

class CommandDefinition:
  def __init__(self, modeling_api, id, fields, **kwargs) -> None:
    super
    self.id = id
    self.modeling_api = modeling_api
    self.fields = json.loads(fields)
    for key, value in kwargs.items():
      setattr(self, key, value)

  def __str__(self):
    details = []
    for x in self.__dict__:
      if x not in ["id", "name", "modeling_api"]:
        key = x
        value = self.__dict__[x]
        try:
          value = value.replace("\n", "")
        except AttributeError:
          pass
        details.append(f"  {key:<20}{value}")

    return f"Command Definition #{self.id}: {self.commandType}\n" + "\n".join(details)

  def to_json(self):
    output = {self.commandType: {}}
    for x in self.__dict__:
      if x not in ["id", "starred", "commandType", "modeling_api"]:
        output[self.commandType][camel_to_snake(x)] = self.__dict__[x]
    return json.dumps(output)

  def update_description(self, new_description):
    cp = copy.copy(self)
    cp.description = new_description
    return self.modeling_api.scripting_api.mutations.update_command_definition(self.id, cp.to_json())

  def update_star(self, starred):
    return self.modeling_api.scripting_api.mutations.star_command_definition(self.id, bool(starred))

  def update_definition(self, new_definition):
    assert isinstance(new_definition, str), "new_definition should be a json string"
    return self.modeling_api.scripting_api.mutations.update_command_definition(self.id, new_definition)
import json
from majortom_scripting.mutations import Mutations

class CommandDefinition:
  def __init__(self, api, id, fields, **kwargs) -> None:
    super
    self.id = id
    self.api = api
    self.fields = json.loads(fields)
    self.mutations = Mutations(api)
    for key, value in kwargs.items():
      setattr(self, key, value)

  def __str__(self):
    details = []
    for x in self.__dict__:
      if x not in ["id", "name", "mutations", "api"]:
        key = x
        value = self.__dict__[x]
        try:
          value = value.replace("\n", "")
        except AttributeError:
          pass
        details.append(f"  {key:<20}{value}")

    return f"Command Definition #{self.id}: {self.commandType}\n" + "\n".join(details)


from majortom_scripting.models.Pass import Pass
from majortom_scripting.models.command_definition import CommandDefinition
from majortom_scripting.exceptions import PassNotFoundError, CommandNotFoundError

from datetime import datetime

class System:
  def __init__(self, modeling_api, id, name, **kwargs) -> None:
    super
    self.id = id
    self.name = name
    self.modeling_api = modeling_api
    self._passes = None
    self._command_definitions = None
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

    return f"Satellite #{self.id}: {self.name}\n" + "\n".join(details)

  @property
  def passes(self):
    self.get_passes(limit=10)
    return self._passes
  
  def get_passes(self, start=None, end=None, limit=100):
    start_time = start if start else datetime.timestamp(datetime.now()) * 1000   # default to upcoming passes
    result = self.modeling_api.scripting_api.passes(system_id=self.id, start_time=start_time, end_time=end, first=limit)
    self._passes = [Pass(self.modeling_api, **x) for x in result["passes"]["nodes"]]
    return self._passes

  def get_upcoming_passes(self, current_unix_time_ms=None):
    now = current_unix_time_ms if current_unix_time_ms else datetime.timestamp(datetime.now()) * 1000
    return self.get_passes(start=now)

  def next_pass(self, current_unix_time_ms=None, scheduled=False):
    future_passes = self.get_upcoming_passes(current_unix_time_ms)
    scheduled_passes = [x for x in future_passes if x.scheduledStatus == "scheduled"] if scheduled else future_passes
    if  len(scheduled_passes) == 0:
      raise PassNotFoundError
    return scheduled_passes[0]

  def get_command_definition(self, command_name):
    try:
      return next((x for x in self.command_definitions if x.commandType == command_name))
    except StopIteration:
      raise CommandNotFoundError

  @property
  def command_definitions(self):
    result = self.modeling_api.scripting_api.command_definitions(systemId=self.id)
    self._command_definitions = [CommandDefinition(self.modeling_api, **x) for x in result]
    return self._command_definitions
    
  def update_command_definitions(self, new_command_defs):
    print(f"Updating command defs for {self.name}")
    return self.modeling_api.scripting_api.mutations.update_command_definitions(self.id, new_command_defs)


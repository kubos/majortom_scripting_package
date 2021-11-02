import logging
from majortom_scripting.mutations import Mutations
from majortom_scripting.models.command import Command
from datetime import datetime

# The file containing this class is capitalized because "pass" is a reserved word.
class Pass:
  def __init__(self, modeling_api, id, start, end, **kwargs) -> None:
    super
    self.id = id
    self.modeling_api = modeling_api
    self.start = start
    self.end = end
    self.mutations = Mutations(modeling_api)
    for key, value in kwargs.items():
      setattr(self, key, value)

  def __str__(self):
    details = []
    for x in self.__dict__:
      if x not in ["id", "name", "mutations", "modeling_api"]:
        key = x
        value = self.__dict__[x]
        try:
          value = value.replace("\n", "")
        except AttributeError:
          pass
        details.append(f"  {key:<20}{value}")
    details.append(self.pretty_print_pass_time())

    return f"Pass #{self.id}:\n" + "\n".join(details)

  def pretty_print_pass_time(self):
    now = datetime.timestamp(datetime.now())*1000
    delta = (self.start - now)/1000.0/60.0
    return f"The pass will start in {delta:.1f} minutes"

  def refresh(self):
    updated_pass = self.modeling_api.scripting_api.apass(self.id)
    for key, value in updated_pass.items():
      setattr(self, key, value)

  def schedule_command(self, command_definition, fields={}):
    logging.info(f"Scheduling Command {command_definition.commandType}")
    return self.mutations.create_and_schedule_command(self.id, self.satellite['id'], command_definition_id=command_definition.id, fields=fields)

  def get_scheduled_commands(self):
    self.refresh()
    if len(self.buckets) > 0:
      return [Command(api=self.modeling_api, **x) for x in self.buckets[0]['sequence']['commands']]
    else:
      return []

  def unschedule_command(self, command):
    logging.info(f"Unscheduling Command #{command.id} - {command.commandType}")
    return self.mutations.unschedule_command(command.id)

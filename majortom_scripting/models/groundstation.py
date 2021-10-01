class GroundStation(dict):
  def __init__(self, modeling_api, id, name, **kwargs) -> None:
    super
    self.id = id
    self.name = name
    self.modeling_api = modeling_api
    for key, value in kwargs.items():
      setattr(self, key, value)

  def __str__(self):
    details = []
    for x in self.__dict__:
      if x not in ["id", "name", "latitude", "longitude", "modeling_api"]:
        key = x
        value = self.__dict__[x]
        try:
          value = value.replace("\n", "")
        except AttributeError:
          pass
        details.append(f"  {key:<20}{value}")
    details.append(self.pretty_print_pass_time())

    return f"Groundstation #{self.id}: {self.name} ({self.latitude},{self.longitude}\n" + "\n".join(details)

  def get_command_def(self):
    return self.api.command_definition(id=self.id, return_fields=["id","description","commandType","displayName","fields","starred","tags"])

  def update_command_definitions(self, new_command_defs):
    print(f"Updating command defs for {self.name}")
    self.mutations.update_command_definitions(self.id, new_command_defs)

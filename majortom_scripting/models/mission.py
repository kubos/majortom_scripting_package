from majortom_scripting.mutations import Mutations
from majortom_scripting.models.satellite import Satellite
from majortom_scripting.models.groundstation import GroundStation

class Mission:
  def __init__(self, api, id, **kwargs) -> None:
    super
    self.id = id
    self.api = api
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

    return f"Mission #{self.id}: {self.name}\n" + "\n".join(details)

  def satellite(self, id=None, name=None):
      return_fields=["id","name","type","noradId","tle","enableTleAutoUpdate","lastTelemetryAt","settings","defaultGatewayId"]
      result = self.api.scripting_api.system(id, name, return_fields=return_fields)
      return Satellite(modeling_api=self.api, **result) 

  def satellites(self):
    return_fields = ["id","name","type","noradId","tle","enableTleAutoUpdate","lastTelemetryAt","settings","defaultGatewayId"]
    result = self.api.scripting_api.satellites(return_fields=return_fields)
    return [Satellite(modeling_api=self.api, **x["node"]) for x in result]

  def groundstation(self, id=None, name=None):
    return_fields = ["id","name","type","latitude","longitude","lastTelemetryAt","settings","defaultGatewayId"]
    result = self.api.scripting_api.system(id, name, return_fields=return_fields)
    return GroundStation(modeling_api=self.api, **result)

  def groundstations(self):
    return_fields = ["id","name","type","latitude","longitude"]
    result = self.api.scripting_api.groundstations(return_fields=return_fields)
    return [GroundStation(modeling_api=self.api, **x["node"]) for x in result]

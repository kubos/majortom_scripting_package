from requests.api import request
from majortom_scripting.models.groundstation import GroundStation
import logging
from majortom_scripting import ScriptingAPI
from majortom_scripting.exceptions import ApiError, UnknownObjectError
from majortom_scripting.models.mission import Mission
from majortom_scripting.models.satellite import Satellite
from majortom_scripting.models.groundstation import GroundStation
from majortom_scripting.models.Pass import Pass

logger = logging.getLogger(__name__)


class ModelingAPI:
    def __init__(self, host, token, scheme="https", port=None, basic_auth_username=None, basic_auth_password=None):
      self.scripting_api = ScriptingAPI(host, token, scheme, port, basic_auth_username, basic_auth_password)

    # LOW-LEVEL PASS THROUGHS

    def query(self, *args, **kwargs):
      return self.scripting_api.query(*args, **kwargs)

    # HIGH-LEVEL QUERIES

    def mission(self, id):
      return_fields=["id","name"]
      result = self.scripting_api.mission(id, return_fields=return_fields)
      return Mission(self, **result)
      pass

    def missions(self):
      # tbd
      pass

    def satellite(self, id=None, name=None):
        return_fields=["id","name","type","noradId","tle","enableTleAutoUpdate","lastTelemetryAt","settings","defaultGatewayId"]
        result = self.scripting_api.system(id, name, return_fields=return_fields)
        return Satellite(self, **result) 

    def satellites(self):
      return_fields = ["id","name","type","noradId","tle","enableTleAutoUpdate","lastTelemetryAt","settings","defaultGatewayId"]
      result = self.scripting_api.satellites(return_fields=return_fields)
      return [Satellite(self, **x["node"]) for x in result]

    def groundstation(self, id=None, name=None):
      return_fields = ["id","name","type","latitude","longitude","lastTelemetryAt","settings","defaultGatewayId"]
      result = self.scripting_api.system(id, name, return_fields=return_fields)
      return GroundStation(self, **result)

    def groundstations(self):
      return_fields = ["id","name","type","latitude","longitude"]
      result = self.scripting_api.groundstations(return_fields=return_fields)
      return [GroundStation(self, **x["node"]) for x in result]

    def apass(self, passId):
      """Lookup a pass by id. The method name is a little strange because 'pass' is a reserved word in Python. """
      result = self.scripting_api.apass(passId)
      return Pass(self, **result)



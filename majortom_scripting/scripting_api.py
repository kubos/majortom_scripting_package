from requests.api import request
import requests
import logging
import json
import datetime
from majortom_scripting.mutations import Mutations
from majortom_scripting.exceptions import ApiError, QueryError, UnknownObjectError, ScriptDisabledError, TokenInvalidError, RateLimitError

logger = logging.getLogger(__name__)


class ScriptingAPI:
    def __init__(self, host, token, scheme="https", port=None, basic_auth_username=None, basic_auth_password=None):
        self.host = host
        self.token = token
        self.scheme = scheme
        self.port = port
        self.basic_auth_username = str(basic_auth_username)
        self.basic_auth_password = str(basic_auth_password)
        self.mutations = Mutations(self)
        self.__script_info = None

    @property
    def script_info(self):
        if self.__script_info is None:
            self.__fetch_script_info()
        return self.__script_info

    def script_id(self):
        return self.script_info['id']

    def mission_id(self):
        return self.script_info['mission']['id']

    def mission(self, id, return_fields=[]):
        """Lookup a Mission by id"""

        default_fields = ['id', 'name']

        graphql = """
            query MissionQuery($id: ID!) {
                mission(id: $id) {
                    %s
                }
            }
        """ % ', '.join(set().union(default_fields, return_fields))

        request = self.query(graphql,
                             variables={'id': id},
                             path='data.mission')

        if request is None:
            raise UnknownObjectError(object="mission", id=id)

        return request

    def system(self, id=None, name=None, return_fields=[]):
        """Lookup a system by id or name"""

        default_fields = ['id', 'name']

        graphql = """
            query SystemQuery($id: ID, $missionId: ID, $name: String) {
                system(id: $id, missionId: $missionId, name: $name) {
                    %s
                }
            }
        """ % ', '.join(set().union(default_fields, return_fields))

        request = self.query(graphql,
                             variables={
                                 'id': id,
                                 'missionId': self.mission_id(),
                                 'name': name
                             },
                             path='data.system')

        if request is None:
            if id:
                raise UnknownObjectError(object="system", id=id)
            else:
                raise UnknownObjectError(object="system", name=name)

        return request

    def subsystem(self, id=None, system_name=None, name=None, return_fields=[]):
        """Lookup a subsystem by id or system_name and name"""

        default_fields = ['id', 'name']

        graphql = """
            query SubsystemQuery($id: ID, $missionId: ID, $systemName: String, $name: String) {
                subsystem(id: $id, missionId: $missionId, systemName: $systemName, name: $name) {
                    %s
                }
            }
        """ % ', '.join(set().union(default_fields, return_fields))

        request = self.query(graphql,
                             variables={
                                 'id': id,
                                 'missionId': self.mission_id(),
                                 'systemName': system_name,
                                 'name': name
                             },
                             path='data.subsystem')

        if request is None:
            if id:
                raise UnknownObjectError(object="subsystem", id=id)
            else:
                raise UnknownObjectError(object="subsystem", name=name, parent=system_name)

        return request

    def metric(self, id=None, system_name=None, subsystem_name=None, name=None, return_fields=[]):
        """Lookup a metric by id or system_name, subsystem_name, and name"""

        default_fields = ['id', 'name']

        graphql = """
            query MetricQuery($id: ID, $missionId: ID, $systemName: String, $subsystemName: String, $name: String) {
                metric(id: $id, missionId: $missionId, systemName: $systemName, subsystemName: $subsystemName, name: $name) {
                    %s
                }
            }
        """ % ', '.join(set().union(default_fields, return_fields))

        request = self.query(graphql,
                             variables={
                                 'id': id,
                                 'missionId': self.mission_id(),
                                 'systemName': system_name,
                                 'subsystemName': subsystem_name,
                                 'name': name},
                             path='data.metric')

        if request is None:
            if id:
                raise UnknownObjectError(object="metric", id=id)
            else:
                raise UnknownObjectError(object="metric", name=name, parent=subsystem_name)

        return request

    def command_definition(self, id=None, system_name=None, command_type=None, return_fields=[]):
        """Lookup a command definition by id or system_name and command type"""

        default_fields = ['id', 'displayName', 'commandType', 'fields']

        graphql = """
            query CommandDefinitionQuery($id: ID,$missionId: ID, $systemName: String, $commandType: String) {
                commandDefinition(id: $id, missionId: $missionId, systemName: $systemName, commandType: $commandType) {
                    %s
                }
            }
        """ % ', '.join(set().union(default_fields, return_fields))

        request = self.query(graphql,
                             variables={
                                 'id': id,
                                 'missionId': self.mission_id(),
                                 'systemName': system_name,
                                 'commandType': command_type
                             },
                             path='data.commandDefinition')

        if request is None:
            if id:
                raise UnknownObjectError(object="command_definition",
                                         id=id)
            else:
                raise UnknownObjectError(object="command_definition",
                                         name=command_type,
                                         parent=system_name)

        return request

    def command_definitions(self, systemId, return_fields=[]):
        """ Look up all command definitions on a system"""

        default_fields = ['id', 'description', 'commandType', 'displayName', 'fields', 'starred', 'tags']

        graphql = """
            query CommandsDefinitionsForSystemQuery($systemId: ID!) {
                system(id: $systemId) {
                    commandDefinitions {
                        nodes {
                            %s
                        }
                    }
                }
            }
        """ % ', '.join(set().union(default_fields, return_fields))

        request = self.query(graphql,
                             variables={
                                 'systemId': systemId,
                             },
                             path='data.system.commandDefinitions.nodes')

        if request is None:
            raise UnknownObjectError(object="system", id=systemId)

        return request


    def command(self, id, return_fields=[]):
        """Lookup a command by id"""

        default_fields = ['id', 'commandType', 'fields', 'state']

        graphql = """
            query CommandQuery($id: ID!) {
                command(id: $id) {
                    %s
                }
            }
        """ % ', '.join(set().union(default_fields, return_fields))

        request = self.query(graphql,
                             variables={'id': id},
                             path='data.command')

        if request is None:
            raise UnknownObjectError(object="command", id=id)

        return request

    def commands(self, system_id, states=[], first=10, after_cursor=None, return_fields=[]):
        """Lookup commands by system_id"""

        default_fields = ['id', 'commandType', 'fields', 'state']

        graphql = """
            query CommandsQuery($systemId: ID!, $states: [CommandState!], $first: Int!, $afterCursor: String) {
                system(id: $systemId) {
                    commands(filters: { state: $states },
                             orderBy: { sort: ID, direction: DESC },
                             first: $first,
                             after: $afterCursor) {
                        nodes {
                            %s
                        }
                        pageInfo {
                            hasNextPage, hasPreviousPage, startCursor, endCursor
                        }
                        totalCount
                    }
                }
            }
        """ % ', '.join(set().union(default_fields, return_fields))

        request = self.query(graphql,
                          variables={'systemId': system_id, 'states': states,
                                     'first': first, 'afterCursor': after_cursor},
                          path='data.system.commands')

        if request is None:
            raise UnknownObjectError(object="system", id=system_id)

        return request

    def gateway(self, id=None, name=None, return_fields=[]):
        """Lookup a gateway by id or name"""

        default_fields = ['id', 'name', 'connected']

        graphql = """
            query GatewayQuery($id: ID, $missionId: ID, $name: String) {
                gateway(id: $id, missionId: $missionId, name: $name) {
                    %s
                }
            }
        """ % ', '.join(set().union(default_fields, return_fields))

        request = self.query(graphql,
                             variables={
                                 'id': id,
                                 'missionId': self.mission_id(),
                                 'name': name
                             },
                             path='data.gateway')

        if request is None:
            if id:
                raise UnknownObjectError(object="gateway", id=id)
            else:
                raise UnknownObjectError(object="gateway", name=name)

        return request

    def events(self, system_id, levels=None, start_time=None, first=10, after_cursor=None, return_fields=[]):
        """Lookup events by system_id"""

        if levels is None:
            levels = ['debug', 'deprecated', 'nominal', 'warning', 'error', 'critical']

        if start_time is None:
            start_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=15)

        start_time_in_epoch_millis = (
            start_time - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000.0

        default_fields = ['id', 'type', 'message', 'level', 'timestamp']

        graphql = """
            query EventsQuery($missionId: ID!, $systemId: [ID!], $levels: [EventLevel!], $startTime: Time!, $first: Int!, $afterCursor: String) {
                mission(id: $missionId) {
                    events(filters: { systemId: $systemId, level: $levels, startTime: $startTime },
                           orderBy: { sort: TIMESTAMP, direction: ASC },
                           first: $first,
                           after: $afterCursor) {
                        nodes {
                            %s
                        }
                        pageInfo {
                            hasNextPage, hasPreviousPage, startCursor, endCursor
                        }
                        totalCount
                    }
                }
            }
        """ % ', '.join(set().union(default_fields, return_fields))

        return self.query(graphql,
                          variables={'missionId': self.mission_id(),
                                     'systemId': [system_id],
                                     'levels': levels,
                                     'first': first,
                                     'startTime': start_time_in_epoch_millis,
                                     'afterCursor': after_cursor},
                          path='data.mission.events')

    def satellites(self, return_fields = []):
        default_fields = ["id","name","type","noradId","tle","enableTleAutoUpdate","lastTelemetryAt","settings","defaultGatewayId"]

        graphql = """
            query GetSystems (
                $missionId: ID!,
                $systemFilters: SystemFilter,
                ) {
                mission(id: $missionId) {
                    id
                    systems(filters: $systemFilters, orderBy: { sort: NAME, direction: ASC }) {
                    edges {
                        node {
                            %s
                        }
                    }
                    }
                }
            }
        """ % ', '.join(set().union(default_fields, return_fields))

        response = self.query(graphql,
                             variables={
                                'missionId': self.mission_id(),
                                'systemFilters': {"type": "Satellite"}
                             },
                             path='data.mission.systems.edges')

        if response is None:
            raise ApiError("Unknown error")

        return response

    def groundstations(self, return_fields = []):
        default_fields = ["id","name","type","latitude","longitude"]

        graphql = """
            query GetSystems (
                $missionId: ID!,
                $systemFilters: SystemFilter,
                ) {
                mission(id: $missionId) {
                    id
                    systems(filters: $systemFilters, orderBy: { sort: NAME, direction: ASC }) {
                    edges {
                        node {
                            %s
                        }
                    }
                    }
                }
            }
        """ % ', '.join(set().union(default_fields, return_fields))

        response = self.query(graphql,
                             variables={
                                'missionId': self.mission_id(),
                                'systemFilters': {"type": "GroundStation"}
                             },
                             path='data.mission.systems.edges')

        if response is None:
            raise ApiError("Unknown error")

        return response

    def apass(self, passId):
        graphql = """
            query PassQuery($passId: ID!) {
                pass(id: $passId) {
                    id
                    start
                    end
                    scheduledStatus
                    satellite { id }
                    groundStation { id }
                    maxElevation
                    nextSatPassId
                    prevSatPassId
                    nextGsPassId
                    prevGsPassId
                    nextPassId
                    prevPassId
                    buckets {
                        id
                        attachedToId
                        attachedToType
                        sequence {
                            id
                            commands {
                                id
                                state
                                commandType
                                displayName
                                description
                                fields
                                commandDefinition { id }
                                sequenceOrder
                            }
                        }   
                    }
                }
            }
        """

        response = self.query(graphql,
                             variables={'passId': passId},
                             path='data.pass')

        if response is None:
            raise UnknownObjectError(object="pass", id=id)

        return response

    def query(self, query, variables=None, operation_name=None, path=None):
        logger.debug(query)
        if self.port is None:
            url = f"{self.scheme}://{self.host}/script_api/v1/graphql"
        else:
            url = f"{self.scheme}://{self.host}:{self.port}/script_api/v1/graphql"

        request = requests.post(url,
                                auth=(self.basic_auth_username, self.basic_auth_password),
                                headers={
                                    'X-Script-Token': self.token,
                                },
                                json={
                                    'query': query,
                                    'variables': variables,
                                    'operationName': operation_name
                                })

        if request.status_code == 422:
            raise ScriptDisabledError()
        elif request.status_code == 420:
            raise RateLimitError(reset_after=request.headers['x-ratelimit-resetafter'],
                                 retry_after=request.headers['x-ratelimit-retryafter'],
                                 errors=request.json()["errors"])
        elif request.status_code == 403:
            raise TokenInvalidError()

        request.raise_for_status()

        json_result = request.json()
        logger.debug(json.dumps(json_result, indent=2))

        if 'errors' in json_result:
            raise QueryError(request=request, errors=json_result["errors"])

        if path:
            for s in path.split('.'):
                if json_result:
                    json_result = json_result.get(s)

        return json_result

    def check_user_connection(self):
        return self.query("""
            query Status {
                agent {
                    type
                    user { name }
                    script { name }
                }
            }
        """, path='data.agent.user')

    def __fetch_script_info(self):
        self.__script_info = self.query("""
            query {
                agent {
                    type
                    script {
                        name, id
                        mission { name, id }
                    }
                }
            }
        """, path='data.agent.script')

        logger.info(f"Script Info: {self.script_info}")

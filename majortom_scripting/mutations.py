import logging
import json

from majortom_scripting.exceptions import ApiError, MutationError

logger = logging.getLogger(__name__)


class Mutations:
    def __init__(self, api):
        self.api = api

    def create_and_schedule_command(self, passId, system_id, command_definition_id, fields={}, bucketType="During", attachedToType="Transit", order=None, return_fields=[]):
        default_fields = ['id', 'commandType', 'fields', 'state']

        graphql = """
            mutation ScheduleCommandMutation($bucketId: ID, $passId: ID, $bucketType: BucketType, $attachedToType: BucketAttachedToType, $order: Int, $systemId: ID!, $commandDefinitionId: ID!, $fields: Json!) {
                scheduleCommandMutation(input: { bucketId: $bucketId, passId: $passId, bucketType: $bucketType, attachedToType: $attachedToType, order: $order, systemId: $systemId, commandDefinitionId: $commandDefinitionId, fields: $fields }) {
                    success
                    errors
                    notice
                    command {
                        %s
                    }
                }
            }
        """% ', '.join(set().union(default_fields, return_fields))

        variables = {
            "passId": passId,
            'systemId': system_id,
            'commandDefinitionId': command_definition_id,
            "bucketType": bucketType, 
            "attachedToType": attachedToType,
            'fields': json.dumps(fields),
        }

        if order is not None:
            variables["order"] = order

        request = self.api.query(graphql,
                                 variables=variables,
                                 path='data.scheduleCommandMutation')

        if request is None:
            raise(ApiError())

        if not request["success"]:
            logger.error(request["errors"])
            raise(MutationError(request=request))

        logger.info(request["notice"])
        return request

    def unschedule_command(self, commandId):
        graphql = """
            mutation UnscheduleCommandMutation ($commandId:ID!) {
                unscheduleCommandMutation(input: { id: $commandId }) {
                    success
                    errors
                    notice
                }
            }
        """
        variables = {
            "commandId": commandId,
        }

        request = self.api.query(graphql,
                                 variables=variables,
                                 path='data.unscheduleCommandMutation')

        if request is None:
            raise(ApiError())

        if not request["success"]:
            logger.error(request["errors"])
            raise(MutationError(request=request))

        logger.info(request["notice"])
        return request

    def queue_and_execute_command(self, system_id, command_definition_id, gateway_id, fields={}, return_fields=[]):
        default_fields = ['id', 'commandType', 'fields', 'state']

        graphql = """
            mutation QueueAndExecuteCommand($systemId: ID!, $commandDefinitionId: ID!, $gatewayId: ID!, $fields: Json) {
                queueAndExecuteCommand(input: { systemId: $systemId, commandDefinitionId: $commandDefinitionId, gatewayId: $gatewayId, fields: $fields }) {
                    success notice errors
                    command {
                        %s
                    }
                }
            }
        """ % ', '.join(set().union(default_fields, return_fields))

        request = self.api.query(graphql,
                                 variables={
                                     'systemId': system_id,
                                     'commandDefinitionId': command_definition_id,
                                     'gatewayId': gateway_id,
                                     'fields': json.dumps(fields)
                                 },
                                 path='data.queueAndExecuteCommand')

        if not request["success"]:
            raise(MutationError(request=request))

        logger.info(request["notice"])
        return request

    def queue_command(self, system_id, command_definition_id, gateway_id, fields={}, return_fields=[]):
        default_fields = ['id', 'commandType', 'fields', 'state']

        graphql = """
            mutation QueueCommand($systemId: ID!, $commandDefinitionId: ID!, $gatewayId: ID!, $fields: Json) {
                queueCommand(input: { systemId: $systemId, commandDefinitionId: $commandDefinitionId, gatewayId: $gatewayId, fields: $fields }) {
                    success notice errors
                    command {
                        %s
                    }
                }
            }
        """ % ', '.join(set().union(default_fields, return_fields))

        request = self.api.query(graphql,
                                 variables={
                                     'systemId': system_id,
                                     'commandDefinitionId': command_definition_id,
                                     'gatewayId': gateway_id,
                                     'fields': json.dumps(fields)
                                 },
                                 path='data.queueCommand')

        if not request["success"]:
            raise(MutationError(request=request))

        logger.info(request["notice"])
        return request

    def execute_command(self, id, return_fields=[]):
        default_fields = ['id', 'commandType', 'fields', 'state']

        graphql = """
            mutation ExecuteCommand($id: ID!) {
                executeCommand(input: { id: $id }) {
                    success notice errors
                    command {
                        %s
                    }
                }
            }
        """ % ', '.join(set().union(default_fields, return_fields))

        request = self.api.query(graphql,
                                 variables={'id': id},
                                 path='data.executeCommand')

        if not request["success"]:
            raise(MutationError(request=request))

        logger.info(request["notice"])
        return request

    def cancel_command(self, id, return_fields=[]):
        default_fields = ['id', 'commandType', 'fields', 'state']

        graphql = """
            mutation CancelCommand($id: ID!) {
                cancelCommand(input: { id: $id }) {
                    success notice errors
                    command {
                        %s
                    }
                }
            }
        """ % ', '.join(set().union(default_fields, return_fields))

        request = self.api.query(graphql,
                                 variables={'id': id},
                                 path='data.cancelCommand')

        if not request["success"]:
            raise(MutationError(request=request))

        logger.info(request["notice"])
        return request

    def update_command_definitions(self, system_id, definitions):
        graphql = """
            mutation UpdateCommandDefinitions($definitions: String, $systemId: ID!) {
                updateCommandDefinitions(input: {definitions: $definitions, systemId: $systemId}){
                    success
                    notice
                    errors
                }
            }
        """

        request = self.api.query(graphql,
                                 variables={
                                     'definitions': definitions,
                                     'systemId': system_id,
                                 },
                                 path='data.updateCommandDefinitions')

        if not request["success"]:
            raise(MutationError(request=request))

        logger.info(request["notice"])
        return request

    def star_command_definition(self, id, starred):
        graphql = """
            mutation UpdateCommandDefinition($id:ID!, $starred:Boolean) {
                updateCommandDefinition(input: {id:$id, starred:$starred}){
                    success
                    notice
                    errors
                }
            }
        """

        request = self.api.query(graphql,
                                 variables={
                                     'id': id,
                                     'starred': bool(starred),
                                 },
                                 path='data.updateCommandDefinition')

        if not request["success"]:
            raise(MutationError(request=request))

        logger.info(request["notice"])
        return request


    def update_command_definition(self, id, new_definition_json: str):
        assert isinstance(new_definition_json, str), 'new_definition_json should be a string!'
        graphql = """
            mutation UpdateCommandDefinition($id:ID!, $definition:Json) {
                updateCommandDefinition(input: {id:$id, definition:$definition}){
                    success
                    notice
                    errors
                }
            }
        """
        request = self.api.query(graphql,
                                 variables={
                                     'id': int(id),
                                     'definition': new_definition_json,
                                 },
                                 path='data.updateCommandDefinition')

        if not request["success"]:
            raise(MutationError(request=request))

        logger.info(request["notice"])
        return request
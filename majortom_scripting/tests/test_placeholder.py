from datetime import datetime
from majortom_scripting.scripting_api import ScriptingAPI
import pytest
from majortom_scripting import ModelingAPI
import logging
import random

@pytest.fixture()
def modeling_api():
    token = "3225eff9f1d40bc1eff70bab51c037e63023977a63e549bb1d2210966c6cfafa"
    host = "host.docker.internal"
    return ModelingAPI(host=host, token=token, scheme="http", port=3001)

@pytest.fixture()
def scripting_api():
    token = "3225eff9f1d40bc1eff70bab51c037e63023977a63e549bb1d2210966c6cfafa"
    host = "host.docker.internal"
    return ScriptingAPI(host=host, token=token, scheme="http", port=3001)


def test_logging_output():
    # A simple test to see what output is being captured
    # Note that pytest typically prints logging messages only when a test fails
    logging.debug("DEBUG: Testing")
    logging.info("INFO: Testing")
    logging.warning("WARN: Testing")
    logging.error("ERROR: Testing")
    print("PRINT: Testing")
    # assert False

def pretty_print_pass(aPass):
    now = datetime.timestamp(datetime.now())*1000
    delta = (aPass.start - now)/1000.0/60.0
    print(f"The pass will start in {delta:.1f} minutes")
    print(aPass)

@pytest.mark.skip(reason="move to example python scripts")
def test_get_command_defs(modeling_api):
    mission = modeling_api.mission(6)
    sat = mission.satellite(name="AQUA")
    defs = sat.command_definitions
    assert len(defs) >= 1

@pytest.mark.skip(reason="move to example python scripts")
def test_update_command_definitions(modeling_api):
    mission = modeling_api.mission(6)
    sat = mission.satellite(name="AQUA")
    import os
    print(os.getcwd())
    with open('majortom_scripting/tests/command_def.json') as f:
        new_defs = f.read()

    retval = sat.update_command_definitions(new_defs)
    assert retval['success'] == True

@pytest.mark.skip(reason="move to example python scripts")
def test_update_single_command_definition(modeling_api):
    # Get definitions
    mission = modeling_api.mission(6)
    sat = mission.satellite(name="AQUA")
    defs = sat.command_definitions

    # Descriptions for chosen command to start with a random number
    cmd_name = "attitude_control"
    my_cmd = (next(x for x in defs if x.commandType == cmd_name))
    print(my_cmd)
    result = my_cmd.update_description(f"{random.randint(0,100)}: {my_cmd.description}")
    print(result)

@pytest.mark.skip(reason="move to example python scripts")
def test_star_definitions(modeling_api):
    # Get definitions
    mission = modeling_api.mission(6)
    sat = mission.satellite(name="AQUA")
    defs = sat.command_definitions

    # Flip all stars
    for definition in defs:
        result = definition.update_star(not(definition.starred))
        print(result)

@pytest.mark.skip(reason="move to example python scripts")
def test_low_level_api_by_getting_tles_for_systems(scripting_api):
    mission_id = 6

    api = scripting_api
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
                    id
                    tle
                }
            }
            }
        }
    }
    """

    response = api.query(graphql,
                        variables={
                        'missionId': mission_id,
                        'systemFilters': {"type": "Satellite", "nameSubstring": "STARLINK"}
                        },
                        path='data.mission.systems.edges')
    # print(response)
    assert len(response) >= 1

@pytest.mark.skip(reason="move to example python scripts")
def test_command_scheduling(modeling_api):
    api = modeling_api

    AQUA = api.satellite(name="AQUA")                        # Get the satellite
    aPass = AQUA.next_pass(scheduled=False)                  # Get the next available, unscheduled pass
    # pretty_print_pass(aPass)
   
    current_commands = aPass.get_scheduled_commands()        # Get the currently-scheduled commands for a pass   
    for command in current_commands:
        result = aPass.unschedule_command(command)           # Unschedule them all
        # print(result['notice'])
   
    ping_command_def = AQUA.get_command_definition("ping")   # Get a specific command definition
    aPass.schedule_command(ping_command_def)                 # Schedule it on a pass

    # Find a random command that has no fields and schedule it
    command_definitions = AQUA.command_definitions           # Get all command defs for that sat
    random_fieldless_command = random.choice([x for x in command_definitions if len(x.fields) == 0])
    aPass.schedule_command(random_fieldless_command)  

    current_commands = aPass.get_scheduled_commands()
    assert len(current_commands) == 2, "There should be commands scheduled"
    assert current_commands[0].commandType == ping_command_def.commandType
    assert current_commands[1].commandType == random_fieldless_command.commandType

@pytest.mark.skip(reason="This test will fail until the backend deploys field integrity verification")
def test_bad_command(modeling_api):
    api = modeling_api

    AQUA = api.satellite(name="AQUA")                        # Get the satellite
    aPass = AQUA.next_pass(scheduled=False)                  # Get the next available, unscheduled pass
   
    # This should fail on account of bad field inputs
    cmd = AQUA.get_command_definition("uplink_file")        # Get a specific command definition
    aPass.schedule_command(cmd, fields={"random":'jazz'})   # Schedule it on a pass
    #### TBD ------------------------

    current_commands = aPass.get_scheduled_commands()
    assert len(current_commands) == 0
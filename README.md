# Major Tom Script API Package
Python Package for interacting with Major Tom's Scripting API. 

The Package contains both a **high-level** and **low-level** API.

## High-Level API 

*This API is in alpha. Please use with caution.*

The new high-level API aims to make the user experience easier by providing canned methods and models for common operations. We trade both customizability and efficiency for ease-of-use. For example, to schedule a command on an upcoming pass, it is only a few lines of code:

```python
# Customize these to your mission 
token = "your script token"
host = "your_instance.majortom.cloud"
satellite_name = "your already-created satellite"
command_name = "your already-created command"
#-------------------------------------------------

api = ModelingAPI(host=host, token=token)                # Create the API
AQUA = api.satellite(name=satellite_name)                # Get the satellite
aPass = AQUA.next_pass()                                 # Get the next pass
definition = AQUA.get_command_definition(command_name)   # Get a specific command
aPass.schedule_command(definition)                       # Schedule it on a pass

```

More examples are available on in our [demo repo](https://github.com/kubos/example-major-tom-scripts).


## Low-Level API

The low-level API provides direct access to the GraphQL query and mutation methods. Users will have to construct a GraphQL query and provide the correct variables in order to use the API. Although it requires more upfront work, the low-level API is the most efficient and customizable way to interact with Major Tom.

Here is an example of retrieving all TLEs from all satellites whose name includes the string "v2" from within a particular mission.

```python
# Customize these to your mission 
token = "your script token"
host = "your_instance.majortom.cloud"
mission_id = 1
#-------------------------------------------------

api = ScriptingAPI(host=host, token=token)
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
                        'systemFilters': {
                          "type": "Satellite", 
                          "nameSubstring": "v2"}
                        },
                        path='data.mission.systems.edges')
    print(response)
```

The GraphQL schema and documentation can be found inside Major Tom on the same page where a Script Token is available. Look for the button labelled "GraphQL Playground".

## Examples 

Example scripts can be found in our [demo repo](https://github.com/kubos/example-major-tom-scripts).

## Development

The Scripting API Package is currently in Beta, so please [give us feedback](https://github.com/kubos/majortom_scripting_package/issues/new) or [come talk to us](https://slack.kubos.com)!

### Testing 

To run all tests, execute `./bin/docker_testw.sh`.
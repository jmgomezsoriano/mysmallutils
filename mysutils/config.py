from typing import Tuple, Any, List


def parse_config(config: dict, params: List[Tuple[str, bool, Any]], double_check: bool = True) -> Tuple:
    """  Check the configuration from a list of parameter definition.

    :param config: The configuration to check.
    :param params: The list of parameter definitions. This list is a tuple with the name of the parameter,
       if the parameter is or not required, and it default value if it is not required. For example, the tuple
       ('server_host', False, 'http://0.0.0.0') defines that the parameter name is 'server_host', that it is not
       required, and if it is not given, then the value is 'http://0.0.0.0'.
    :param double_check: With True, check if all the required configuration parameters are present, and if there are
       any extra parameter which are not present in the parameter definition list. If False, only check the first one:
       if all the required parameters are present.
    :return: The parameter values.
    """
    # Check if there are parameters in the configuration file that are not defined
    if double_check:
        for key in config:
            if key not in [p[0] for p in params]:
                raise ValueError(f'The parameter "{key}" in the configuration file is not a valid parameter.')
    # Check if all required parameters are present in the configuration file
    for key in {p[0] for p in params if p[1]}:
        if key not in config:
            raise ValueError(f'The parameter "{key}" is not defined in the configuration file and it is mandatory.')
    # Extract the parameter values
    values = []
    for p in params:
        values.append(config[p[0]] if p[0] in config else p[2])
    return tuple(values)

from subprocess import Popen, PIPE
from typing import Tuple, List, Union
import re


def split_arg_string(command: str) -> List[str]:
    """ Given an argument string this attempts to split it into small command parts.

    :param command: The command to split.
    :return: A list with each  separated command parts.
    """

    rv = []
    for match in re.finditer(r"('([^'\\]*(?:\\.[^'\\]*)*)'"
                             r'|"([^"\\]*(?:\\.[^"\\]*)*)"'
                             r'|\S+)\s*', command, re.S):
        arg = match.group().strip()
        if arg[:1] == arg[-1:] and arg[:1] in '"\'':
            arg = arg[1:-1].encode('ascii', 'backslashreplace').decode('unicode-escape')
        try:
            arg = type(command)(arg)
        except UnicodeError:
            pass
        rv.append(arg)
    return rv


def execute_command(command: Union[List[str], str], input_text: str = '', cwd: str = None) -> Tuple[str, str]:
    """ Execute an external command easily.

    :param command: The command.
    :param input_text: The text of the standard input.
    :param cwd: The working dir.
    :return: A tuple with the standard and error outputs.
    """
    command = split_arg_string(command) if isinstance(command, str) else command
    process = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True, cwd=cwd)

    process.stdin.write(f'{input_text}\n')

    try:
        return process.communicate()
    finally:
        process.stdin.close()

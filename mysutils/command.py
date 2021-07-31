from subprocess import Popen, PIPE
from typing import Tuple, List


def execute_command(command: List[str], input_text: str = '') -> Tuple[str, str]:
    """ Execute an external command easily.

    :param command: The command.
    :param input_text: The text of the standard input.
    :return: A tuple with the standard and error outputs.
    """
    process = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    process.stdin.write(f'{input_text}\n')

    try:
        return process.communicate()
    finally:
        process.stdin.close()

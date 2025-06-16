from sys import stderr
from typing import Union, List, Dict, Iterable


def ask(
        question: str,
        answers: Union[Iterable[str], Dict[str, Iterable[str]]] = ('y', 'n'),
        default: str = None,
        error_msg: str = 'Wrong answer "{answer}". The only valid answers are: {answers}.',
        ignore_case: bool = True
) -> str:
    """ Ask a question through the console.

    :param question: The question to ask.
    :param answers: The valid answers. It could be a list of answers, for example, ['y', 'n'];
        or a dictionary if we want to accept several correct answers, for example,
        {'y': ['y', 'yes', 'affirmative'], 'n': ['n', 'no', 'negative']}.
        This way, it is possible to accept yes and affirmative as "y", and no or negative as 'n'.
        The keys will be the final answer independently of what variant you write.
    :param default: The default value if enter is pressed.
    :param error_msg: The error message if the user does not introduce the right answer.
    :param ignore_case: If ignore the letter case in the answer or not.

    :return: The introduced answer.
    """
    valid_answers = _get_valid_answers(answers, ignore_case)
    if default is not None and default not in valid_answers:
        raise ValueError(f'The default answer "{default}" is not a valid answer: '
                         f'{", ".join(list(valid_answers.keys()))}')
    while True:
        answer = input(question)
        if not answer and default is not None:
            return default
        if answer.lower() in valid_answers and ignore_case:
            return valid_answers[answer.lower()]
        if answer in valid_answers:
            return valid_answers[answer]
        print(error_msg.format(answer=answer, answers=', '.join(list(valid_answers.keys())), file=stderr))


def _get_valid_answers(answers: Union[Iterable[str], Dict[str, Iterable[str]]], ignore_case: bool) -> Dict[str, str]:
    """ Convert the answers in a dictionary with the valid answers as keys.

    :param answers: The valid answers. It could be a list of answers, for example, ['y', 'n'];
        or a dictionary if we want to accept several correct answers, for example,
        {'y': ['y', 'yes', 'affirmative'], 'n': ['n', 'no', 'negative']}.
        This way, it is possible to accept yes and affirmative as "y", and no or negative as 'n'.
        The keys will be the final answer independently of what variant you write.
    :param ignore_case: If ignore the letter case in the answer or not.
    """
    answers = answers if isinstance(answers, Dict) else {answer: answer.lower() for answer in answers}
    valid_answers = {}
    for k, v in answers.items():
        for answer in v:
            valid_answers[answer.lower() if ignore_case else answer] = k
    return valid_answers

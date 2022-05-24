import re
from enum import Enum, unique
from typing import Union

URL_PATTERN = r'[A-Za-z0-9]+://[A-Za-z0-9%-_]+(/[A-Za-z0-9%-_])*(#|\\?)[A-Za-z0-9%-_&=]*'


def remove_urls(text: str, end_with: str = '') -> str:
    """ Remove any url in the text.

    :param text: The text to remove urls.
    :param end_with: If set, only remove the URLs that finish with that regular expression.
        By default, all the URLs are remvoed.
    :return: The same text but without urls.
    """
    return replace_urls(text, '', end_with)


def replace_urls(text: str, replace: str, end_with: str = '') -> str:
    """ Replace all the URLs with path by a text.

    :param text: The text to replace.
    :param replace: The text to replace with.
    :param end_with: A regular expression which the URL has to finish with.
         By default, replace all the URLs.
    :return: The replaced text.
    """
    matches = list(re.finditer(URL_PATTERN + end_with, text))
    matches.reverse()
    for match in matches:
        start, end = match.span()[0], match.span()[1]
        text = text[:start] + replace + text[end:]
    return text


def clean_text(text: str, lower: bool = True, url: bool = True) -> str:
    """ Remove punctuation symbols, urls and convert to lower.

    :param text: The text to clean.
    :param lower: If you want to convert to lower.
    :param url: If you want to remove urls.
    :return: The cleaned text.
    """
    text = text.lower() if lower else text
    text = remove_urls(text) if url else text
    text = re.sub(r'[^A-Za-z0-9 -]', ' ', text)
    return re.sub(r'[\s]+', ' ', text).strip()


def color(r: int, g: int, b: int) -> str:
    """ Get a ANSI code for a given (R, G, B) foreground color.

    :param r: A value between 0 and 255 for the red component color.
    :param g: A value between 0 and 255 for the green component color.
    :param b: A value between 0 and 255 for the blue component color.
    :return: A string that represents the ANSI code color.
    """
    return f'\033[38{_color(r, g, b)}m'


def bg_color(r: int, g: int, b: int) -> str:
    """ Get a ANSI code for a given (R, G, B) background color.

    :param r: A value between 0 and 255 for the red component color.
    :param g: A value between 0 and 255 for the green component color.
    :param b: A value between 0 and 255 for the blue component color.
    :return: A string that represents the ANSI code background color.
    """
    return f'\033[48{_color(r, g, b)}m'


def un_color(r: int, g: int, b: int) -> str:
    """ Get a ANSI code for a given (R, G, B) underline color.

    :param r: A value between 0 and 255 for the red component color.
    :param g: A value between 0 and 255 for the green component color.
    :param b: A value between 0 and 255 for the blue component color.
    :return: A string that represents the ANSI code underline color.
    """
    return f'\033[58{_color(r, g, b)}m'


def _color(r: int, g: int, b: int) -> str:
    """ Check if the values are correct and return the part of the ANSI code that represents the (R, G, B) color.

    :param r: A value between 0 and 255 for the red component color.
    :param g: A value between 0 and 255 for the green component color.
    :param b: A value between 0 and 255 for the blue component color.
    :return: The part of the ANSI code that represents the (R, G, B) color.
    :raises ValueError: If any (R, G, B) values are not between 0 and 255.
    """
    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
        return f';2;{r};{g};{b}'
    raise ValueError(f'The (r, g, b) values must be between 0 and 255. Current values (r={r}, g={g}, b={b}).')


@unique
class AnsiCodes(Enum):
    """ Enumeration with the most relevant ANSI codes for terminals. """
    NORMAL = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    SLOW_BLINK = '\033[5m'
    RAPID_BLINK = '\033[6m'
    INVERT = '\033[7m'
    HIDE = '\033[8m'
    STRIKE = '\033[9m'
    # PRIMARY = '\033[10m'
    # ALTERNATIVE = '\033[13m'
    GOTHIC = '\033[20m'
    DOUBLE = '\033[21m'
    NOT_INTENSITY = '\033[22m'
    NOT_ITALIC = '\033[23m'
    NOT_UNDERLINE = '\033[24m'
    NOT_BLINKING = '\033[25m'
    NOT_REVERSE = '\033[27m'
    NOT_HIDE = '\033[28m'
    NOT_STRIKE = '\033[29m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    DEFAULT = '\033[39m'
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    BG_DEFAULT = '\033[49m'
    DEF_UNDERLINE = '\033[59m'
    SUPERSCRIPT = '\033[73m'
    SUBSCRIPT = '\033[74m'
    NOT_SUPER_SUB = '\033[75m'
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    BG_BRIGHT_BLACK = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'
    UN_BLACK = un_color(0, 0, 0)
    UN_RED = un_color(170, 0, 0)
    UN_GREEN = un_color(0, 170, 0)
    UN_YELLOW = un_color(170, 85, 0)
    UN_BLUE = un_color(0, 0, 170)
    UN_MAGENTA = un_color(170, 0, 170)
    UN_CYAN = un_color(0, 170, 170)
    UN_WHITE = un_color(170, 170, 170)
    UN_BRIGHT_BLACK = un_color(85, 85, 85)
    UN_BRIGHT_RED = un_color(255, 85, 85)
    UN_BRIGHT_GREEN = un_color(85, 255, 85)
    UN_BRIGHT_YELLOW = un_color(255, 255, 85)
    UN_BRIGHT_BLUE = un_color(85, 85, 255)
    UN_BRIGHT_MAGENTA = un_color(255, 85, 255)
    UN_BRIGHT_CYAN = un_color(85, 255, 255)
    UN_BRIGHT_WHITE = un_color(255, 255, 255)

    @staticmethod
    def get(code: Union['AnsiCodes', str]) -> str:
        """ Return the ANSI code from its code name.

        :param code: An instance of AnsiCodes, the ANSI code name or ANSI color code value.
        :return: A string with the ANSI code value.
        """
        if isinstance(code, AnsiCodes):
            return code.value
        if is_color(code):
            return code
        try:
            return AnsiCodes(code).value
        except ValueError:
            return AnsiCodes[code.upper()].value

    def __contains__(self, code: Union['AnsiCodes', str]) -> bool:
        """ Check if a code is a set ANSI code.

        :param code: An instance of AnsiCodes or the ANSI code name.
        :return: True if it is an ANSI code, False otherwise.
        """
        return isinstance(code, AnsiCodes) or bool(AnsiCodes.get(code))


def markup(text: str, *styles: Union[AnsiCodes, str]) -> str:
    """ The same text but with the ANSI codes for the effects.

    :param text: The text to markup.
    :param styles: The styles.
    :return:
    """
    marks = [AnsiCodes.get(style) for style in styles]
    return ''.join(marks) + text + AnsiCodes.NORMAL.value


def is_color(color_code: str) -> bool:
    """ Check if a color code is a valid ANSI color code.
    :param color_code: The color code to evaluate.
    :return: True if the color is valid, False otherwise.
    """
    return bool(re.match(r'^\033\[(([3-4][0-7]|39|49|59)|(38|48|58);(5;[0-9]+|2;[0-9]+;[0-9]+;[0-9]+))m$', color_code))

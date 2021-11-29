import re
from logging import getLogger
from os.path import exists

from mysutils.file import read_from
from mysutils.service import endpoint

try:
    from markdown import markdown
except ImportError:
    raise ImportError('To use these functions you need to import the markdown module:\n\n'
                      'pip install markdown')

logger = getLogger(__name__)
README = 'README.md'


def gen_service_help(title: str, file: str = README, regex: str = '', *endpoints: str) -> str:
    """ Generate a HTML page from a README file or other Markdown file.

    :param title: The page title.
    :param file: The Markdown file.
    :param regex: A regular expression that determines from which line the markdown has to be processed.
    :param endpoints: The different endpoints of the service.
    :return: The Web page.
    """
    help_text = html_header(title)
    help_text += f'<h1>{title}</h1>' \
                 f'<p><b>Note: </b>Apart of this online help, you may use the <a href="docs">API documentation</a> or ' \
                 f'<a href="redoc">API specification</a>.</p>\n'
    if exists(file):
        readme_text = ''.join(read_from(file, regex)[1:])
        help_text += markdown(readme_text, extensions=['fenced_code', 'codehilite'])
        for e in endpoints:
            help_text = re.sub(f'https?://.*{e}', f'{endpoint(e)}', help_text)
    else:
        logger.warning(f'If you want to show an online help, please, add the file {file} to the project root.')

    help_text += '<p>For more information, see the <a href="docs">API documentation</a> or ' \
                 '<a href="redoc">API specification</a>.</p>\n'
    return help_text + html_footer()


def html_header(title: str) -> str:
    """ Generate a Web page header.
    :param title: The title of the page.
    :return: The HTML of the header.
    """
    return f'<html>\n' \
           f'<head>\n' \
           f'  <title>{title}</title>\n' \
           f'</head>\n' \
           f'<body>\n'


def html_footer():
    """ Generate a Web page footer.
    :return: The HTML of the Web footer.
    """
    return '</body>'

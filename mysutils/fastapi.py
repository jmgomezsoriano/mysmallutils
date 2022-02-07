import re
from logging import getLogger
from os.path import exists

from mysutils.file import read_from
from mysutils.service import endpoint

try:
    from markdown import markdown
except ImportError:
    raise ImportError('To use these functions you need to import the markdown module:\n\n'
                      'pip install markdown==3.3.6\n\n'
                      'Optionally, if you want colourful code, you also need to install Pygments:\n\n'
                      'pip install Pygments>=2.10.0,~=2.11.2')

logger = getLogger(__name__)
try:
    import pygments
except ImportError:
    logger.warning('If you wants to colourful code, please install Pygments:\n\npip install Pygments>=2.10.0,~=2.11.2')

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
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">''' + \
    f'<title>{title}</title>' + \
    '''<style>
        body {
            font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
            color: rgb(33, 37, 41);
            font-size: 16px;
            font-weight: 400;
            line-height: 24px;
            text-align: start;
        }
        h1 {
            box-sizing: border-box;
            font-size: 40px;
            font-weight: 500;
            line-height: 48px;
        }
        h2 {
            font-size: 24px;
            font-weight: 700;
        }
        h3 { font-size: 18.72px; }
        h4 { font-size: 16px; }
        .container {
            box-sizing: border-box;
            margin-left: 34.5px;
            margin-right: 34.5px;
            max-width: 1140px;
            padding-left: 12px;
            padding-right: 12px;
            width: 1140px;
        }
        pre { line-height: 125%; }
        td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
        span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
        td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
        span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
        .hll { background-color: #ffffcc }
        { background: #f8f8f8; }
        .c { color: #408080; font-style: italic } /* Comment */
        .err { border: 1px solid #FF0000 } /* Error */
        .k { color: #008000; font-weight: bold } /* Keyword */
        .o { color: #666666 } /* Operator */
        .ch { color: #408080; font-style: italic } /* Comment.Hashbang */
        .cm { color: #408080; font-style: italic } /* Comment.Multiline */
        .cp { color: #BC7A00 } /* Comment.Preproc */
        .cpf { color: #408080; font-style: italic } /* Comment.PreprocFile */
        .c1 { color: #408080; font-style: italic } /* Comment.Single */
        .cs { color: #408080; font-style: italic } /* Comment.Special */
        .gd { color: #A00000 } /* Generic.Deleted */
        .ge { font-style: italic } /* Generic.Emph */
        .gr { color: #FF0000 } /* Generic.Error */
        .gh { color: #000080; font-weight: bold } /* Generic.Heading */
        .gi { color: #00A000 } /* Generic.Inserted */
        .go { color: #888888 } /* Generic.Output */
        .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
        .gs { font-weight: bold } /* Generic.Strong */
        .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
        .gt { color: #0044DD } /* Generic.Traceback */
        .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
        .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
        .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
        .kp { color: #008000 } /* Keyword.Pseudo */
        .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
        .kt { color: #B00040 } /* Keyword.Type */
        .m { color: #666666 } /* Literal.Number */
        .s { color: #BA2121 } /* Literal.String */
        .na { color: #7D9029 } /* Name.Attribute */
        .nb { color: #008000 } /* Name.Builtin */
        .nc { color: #0000FF; font-weight: bold } /* Name.Class */
        .no { color: #880000 } /* Name.Constant */
        .nd { color: #AA22FF } /* Name.Decorator */
        .ni { color: #999999; font-weight: bold } /* Name.Entity */
        .ne { color: #D2413A; font-weight: bold } /* Name.Exception */
        .nf { color: #0000FF } /* Name.Function */
        .nl { color: #A0A000 } /* Name.Label */
        .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
        .nt { color: #008000; font-weight: bold } /* Name.Tag */
        .nv { color: #19177C } /* Name.Variable */
        .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
        .w { color: #bbbbbb } /* Text.Whitespace */
        .mb { color: #666666 } /* Literal.Number.Bin */
        .mf { color: #666666 } /* Literal.Number.Float */
        .mh { color: #666666 } /* Literal.Number.Hex */
        .mi { color: #666666 } /* Literal.Number.Integer */
        .mo { color: #666666 } /* Literal.Number.Oct */
        .sa { color: #BA2121 } /* Literal.String.Affix */
        .sb { color: #BA2121 } /* Literal.String.Backtick */
        .sc { color: #BA2121 } /* Literal.String.Char */
        .dl { color: #BA2121 } /* Literal.String.Delimiter */
        .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
        .s2 { color: #BA2121 } /* Literal.String.Double */
        .se { color: #BB6622; font-weight: bold } /* Literal.String.Escape */
        .sh { color: #BA2121 } /* Literal.String.Heredoc */
        .si { color: #BB6688; font-weight: bold } /* Literal.String.Interpol */
        .sx { color: #008000 } /* Literal.String.Other */
        .sr { color: #BB6688 } /* Literal.String.Regex */
        .s1 { color: #BA2121 } /* Literal.String.Single */
        .ss { color: #19177C } /* Literal.String.Symbol */
        .bp { color: #008000 } /* Name.Builtin.Pseudo */
        .fm { color: #0000FF } /* Name.Function.Magic */
        .vc { color: #19177C } /* Name.Variable.Class */
        .vg { color: #19177C } /* Name.Variable.Global */
        .vi { color: #19177C } /* Name.Variable.Instance */
        .vm { color: #19177C } /* Name.Variable.Magic */
        .il { color: #666666 } /* Literal.Number.Integer.Long */
    </style>
</head>
<body>
  <div class="container">'''


def html_footer():
    """ Generate a Web page footer.
    :return: The HTML of the Web footer.
    """
    return '</div>\n</body>'

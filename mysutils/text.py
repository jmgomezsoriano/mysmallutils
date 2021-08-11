import re

URL_PATTERN = r'[A-Za-z0-9]+://[A-Za-z0-9%-_]+(/[A-Za-z0-9%-_])*(#|\\?)[A-Za-z0-9%-_&=]*'


def remove_urls(text: str) -> str:
    """ Remove any url in the text.

    :param text: The text to remove urls.
    :return: The same text but without urls.
    """
    return re.sub(URL_PATTERN, '', text)


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

from os import PathLike
from typing import Union

from tqdm.auto import tqdm

try:
    import requests
except ModuleNotFoundError as e:
    raise ModuleNotFoundError('ModuleNotFoundError: No module named \'requests\'. '
                              'Please install it with the command:\n\n'
                              'pip install requests~=2.25.1')


def download(url: str, filename: Union[str, PathLike, bytes], verbose: bool = True) -> None:
    """  Download a file.

    :param url: The URL where the file should be downloaded.
    :param filename: The file path where the file should be stored.
    :param verbose: True, if a progress bar is shown. Otherwise, False.
    """
    request = requests.get(url, stream=True)
    total = int(request.headers['content-length']) if 'content-length' in request.headers else 0
    with request as reader:
        with open(filename, 'wb') as writer:
            with tqdm(desc=f'Downloading file {filename}', total=total, disable=not verbose) as t:
                for chunk in reader.iter_content(chunk_size=8192):
                    t.update(len(chunk))
                    writer.write(chunk)

import requests
from tqdm import tqdm


def download(url: str, fname: str) -> None:
    request = requests.get(url, stream=True)
    total = int(request.headers['content-length']) if 'content-length' in request.headers else 0
    with request as reader:
        with open(fname, 'wb') as writer:
            with tqdm(desc=f'Downloading file {fname}', total=total) as t:
                for chunk in reader.iter_content(chunk_size=8192):
                    t.update(len(chunk))
                    writer.write(chunk)
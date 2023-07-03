import requests
from bs4 import BeautifulSoup

from . import headers


def resolve(url: str) -> dict:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return {'title': soup.title.string}
    raise RuntimeError("resolving error: default")


if __name__ == '__main__':
    print(resolve("https://www.baidu.com"))
import requests

if __name__ == '__main__':
    knodes: list = requests.get(
        url="http://localhost:34443/core/user/0/knode",
        headers={"admin-pass": "$PHYphyPHYphy$"}).json()
    titles: dict = requests.get(
        url="http://localhost:34443/core/knode/1648897276709150208/chainStyleTitleBeneath",
        headers={"admin-pass": "$PHYphyPHYphy$"}).json()
    for pair in titles.items():
        print(pair)

    requests.post("http://localhost:31595/index", json={"knodeIds": [knode["id"] for knode in knodes]})
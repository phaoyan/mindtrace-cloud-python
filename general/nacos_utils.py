import json
import os
import threading
import time

import nacos
import requests

SERVER_HOST = os.getenv('SERVER_HOST')
LOCAL_HOST = os.getenv("LOCAL_HOST")
service_client = nacos.NacosClient(server_addresses=f"{SERVER_HOST}:8848", namespace="public")


def nacos_init(ip: str, port: int, service_name: str):
    requests.post(
        url=f"http://{SERVER_HOST}:8848/nacos/v1/ns/instance",
        params={"ip": ip, "port": port, "serviceName": service_name, "weight": 1.0})

    def heartbeat():
        while True:
            requests.put(
                url=f"http://{SERVER_HOST}:8848/nacos/v1/ns/instance/beat",
                params={
                    "ip": ip, "port": port,
                    "serviceName": service_name,
                    "groupName": "DEFAULT_GROUP",
                    "ephemeral": "true",
                    "beat": json.dumps({
                        "ip": ip,
                        "port": port,
                        "serviceName": service_name
                    })})
            time.sleep(5)

    heartbeat_thread = threading.Thread(target=heartbeat, daemon=True)
    heartbeat_thread.start()

def nacos_service_instance(service_name: str):
    return requests.get(
        url=f"http://{SERVER_HOST}:8848/nacos/v1/ns/instance/list",
        params={
            "serviceName": service_name,
            "groupName": "DEFAULT_GROUP"
        }
    ).json()

def serv_host(service: dict) -> str:
    return f"http://{service['hosts'][0]['ip']}:{service['hosts'][0]['port']}"

def gateway_host() -> str:
    return serv_host(nacos_service_instance("mindtrace-gateway"))


if __name__ == '__main__':

    nacos_init(ip=LOCAL_HOST, port=31595, service_name="mindtrace-knode-similarity-python")

    # requests.delete(
    #     url=f"http://{SERVER_HOST}:8848/nacos/v1/ns/instance",
    #     params={
    #         "ip": LOCAL_HOST,
    #         "port": 31595,
    #         "serviceName": "mindtrace-knode-similarity-python",
    #         "groupName": "DEFAULT_GROUP",
    #         "ephemeral": "false"
    #     }
    # )

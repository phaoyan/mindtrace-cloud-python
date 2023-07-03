import os

from general.nacos_utils import nacos_init
from flask import Flask

app = Flask(__name__)

# 注册服务
nacos_init(ip=os.getenv("LOCAL_HOST"), port=34984, service_name="mindtrace-spider-python")

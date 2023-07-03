import os
import requests

# session设置：登录mindtrace-gateway以通过认证检查
session = requests.Session()
session.headers.update({"admin-pass": os.getenv("MINDTRACE_SECRET")})

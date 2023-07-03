from typing import Callable
from .website_resolve import bilibili, default, mindtrace_hub

WebsiteResolver = Callable[[str], dict]


# 在这里添加一个路由匹配，然后实现resolve函数即可添加一个website解析器
type_map = {
    "bilibili": bilibili.resolve,
    "default": default.resolve,
    "mindtrace hub": mindtrace_hub.resolve
}


def route(_type: str) -> WebsiteResolver:
    r"""
        根据网页类型选择合适的解析器解析网页
    :param _type: 网页类型
    :return: 解析这个网页的函数
    """
    try:
        return type_map[_type]
    except KeyError:
        return lambda f: {"error": "Type Not Matched"}

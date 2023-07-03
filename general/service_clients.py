from general.nacos_utils import gateway_host
from general.session_utils import session


def get_chain_style_title(knode_id) -> str:
    try:
        resp: list[str] = session.get(f"{gateway_host()}/core/knode/{knode_id}/chainStyleTitle").json()
        if resp.__contains__("ROOT"):
            resp.remove("ROOT")
        resp.reverse()
        title = " ".join(resp)
        return title if title != "" else " EMPTY "
    except:
        return "EMPTY"

def knode_check_all() -> list[dict]:
    return session.get(f"{gateway_host()}/core/knode").json()

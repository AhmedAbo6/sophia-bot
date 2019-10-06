from typing import Callable, Optional, Any
from random import choice


def parse_reply(raw_reply: Any, uid: Optional[int] = None, message: Optional[str] = None):
    rv = raw_reply
    max_depth = 5
    depth = 0
    while depth < max_depth:
        if isinstance(rv, list):
            rv = choice(rv)
            depth += 1
            continue
        if isinstance(rv, str):
            return rv
        if isinstance(rv, Callable):
            return rv(uid, message)

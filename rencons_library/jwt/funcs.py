from base64 import b64decode
from datetime import datetime
import json
from uuid import UUID

from rencons_library import DATETIME_STRING_FORMAT
from rencons_library.jwt.main import AccessTokenPayload


def read_access_token_payload(token: str) -> AccessTokenPayload:
    payload = json.loads(b64decode(token.split(".")[1] + '=='))

    return AccessTokenPayload(
        user_ident=UUID(payload["user_ident"]),
        permissions=payload["permissions"],
        gen_dt=datetime.strptime(payload["gen_dt"], DATETIME_STRING_FORMAT),
        exp_dt=datetime.strptime(payload["exp_dt"], DATETIME_STRING_FORMAT),
    )

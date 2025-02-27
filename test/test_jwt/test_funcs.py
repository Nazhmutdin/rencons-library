from uuid import uuid4
from datetime import datetime, timedelta

from rencons_library.jwt import JwtService, AccessTokenPayload, read_access_token_payload


def test_read_access_token_payload(jwt_service: JwtService):

    gen_dt = datetime.now()
    exp_dt = gen_dt + timedelta(minutes=15)

    payload = AccessTokenPayload(
        user_ident=uuid4(),
        gen_dt=gen_dt,
        exp_dt=exp_dt,
        permissions={}
    )

    assert read_access_token_payload(jwt_service.create_access_token(**payload)) == payload

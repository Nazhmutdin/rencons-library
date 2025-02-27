from uuid import uuid4
from datetime import datetime, timedelta

from rencons_library.jwt import JwtService


class TestJwtService: 

    def test_create_access_token(self, jwt_service: JwtService):

        gen_dt = datetime.now()
        exp_dt = gen_dt + timedelta(minutes=15)

        jwt_service.create_access_token(
            user_ident=uuid4(),
            gen_dt=gen_dt,
            exp_dt=exp_dt,
            permissions={
                "ident": uuid4()
            }
        )


    def test_read_access_token(self, jwt_service: JwtService):

        ident = uuid4()
        gen_dt = datetime.now()
        exp_dt = gen_dt + timedelta(minutes=15)

        payload = {
            "user_ident": ident,
            "gen_dt": gen_dt,
            "exp_dt": exp_dt,
            "permissions": {
                "ident": uuid4()
            }
        }

        access_token = jwt_service.create_access_token(**payload)

        assert jwt_service.read_access_token(access_token) == payload


    def test_create_refresh_token(self, jwt_service: JwtService):

        gen_dt = datetime.now()
        exp_dt = gen_dt + timedelta(minutes=15)

        jwt_service.create_refresh_token(
            ident=uuid4(),
            user_ident=uuid4(),
            gen_dt=gen_dt,
            exp_dt=exp_dt
        )


    def test_read_refresh_token(self, jwt_service: JwtService):

        ident = uuid4()
        user_ident = uuid4()
        gen_dt = datetime.now()
        exp_dt = gen_dt + timedelta(minutes=15)

        access_token = jwt_service.create_refresh_token(
            ident=ident,
            user_ident=user_ident,
            gen_dt=gen_dt,
            exp_dt=exp_dt
        )

        payload = {
            "ident": ident,
            "user_ident": user_ident,
            "gen_dt": gen_dt,
            "exp_dt": exp_dt
        }

        assert jwt_service.read_refresh_token(access_token) == payload

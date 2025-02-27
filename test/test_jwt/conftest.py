import pytest 

from rencons_library.jwt import JwtService


@pytest.fixture
def jwt_service() -> JwtService:
    return JwtService(
        "HS256",
        "some_test_key"
    )

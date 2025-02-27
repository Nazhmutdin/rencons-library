from typing import Any, TypedDict, Unpack
from uuid import UUID
from datetime import datetime
from copy import copy

from jose.jwt import encode as jwt_encode, decode as jwt_decode

from rencons_library import DATETIME_STRING_FORMAT


class PermissionDict(TypedDict):
    ident: UUID
    user_ident: UUID

    is_super_user: bool

    personal_data_get: bool
    personal_data_create: bool
    personal_data_update: bool
    personal_data_delete: bool

    personal_naks_certification_data_get: bool
    personal_naks_certification_data_create: bool
    personal_naks_certification_data_update: bool
    personal_naks_certification_data_delete: bool

    ndt_data_get: bool
    ndt_data_create: bool
    ndt_data_update: bool
    ndt_data_delete: bool

    acst_data_get: bool
    acst_data_create: bool
    acst_data_update: bool
    acst_data_delete: bool

    acst_file_download: bool
    acst_file_upload: bool

    personal_naks_certification_file_download: bool
    personal_naks_certification_file_upload: bool

    personal_naks_protocol_file_download: bool
    personal_naks_protocol_file_upload: bool


class AccessTokenPayload(TypedDict):
    user_ident: UUID
    permissions: PermissionDict
    gen_dt: datetime
    exp_dt: datetime


class RefreshTokenPayload(TypedDict):
    ident: UUID
    user_ident: UUID
    gen_dt: datetime
    exp_dt: datetime


class JwtService:
    def __init__(
        self,
        algorithm: str,
        secret_key: str,
    ) -> None:
        self.algorithm = algorithm
        self.secret_key = secret_key

    
    def encode(
        self,
        payload: dict[str, Any]
    ) -> str:
        
        payload = copy(payload)

        payload["gen_dt"] = payload.pop("gen_dt").strftime(DATETIME_STRING_FORMAT)
        payload["exp_dt"] = payload.pop("exp_dt").strftime(DATETIME_STRING_FORMAT)

        return jwt_encode(
            payload,
            self.secret_key,
            self.algorithm
        )
    

    def decode(
        self,
        token: str
    ) -> dict[str, Any]:
        return jwt_decode(
            token,
            self.secret_key,
            self.algorithm
        )
    

    def create_access_token(
        self, 
        **payload: Unpack[AccessTokenPayload]
    ) -> str:
        
        payload["user_ident"] = payload["user_ident"].hex
        payload["permissions"]["ident"] = payload["permissions"]["ident"].hex
        del payload["permissions"]["user_ident"]
        
        return self.encode(
            payload=payload
        )


    def create_refresh_token(
        self,
        **payload: Unpack[RefreshTokenPayload]
    ) -> str:
        payload["user_ident"] = payload["user_ident"].hex
        payload["ident"] = payload["ident"].hex
        
        return self.encode(
            payload=payload
        )
    

    def read_access_token(
        self,
        token: str
    ) -> AccessTokenPayload:
        data = self.decode(token)

        return AccessTokenPayload(
            user_ident=UUID(data["user_ident"]),
            permissions=data["permissions"],
            gen_dt=datetime.strptime(data["gen_dt"], DATETIME_STRING_FORMAT),
            exp_dt=datetime.strptime(data["exp_dt"], DATETIME_STRING_FORMAT),
        )
    

    def read_refresh_token(
        self,
        token: str
    ) -> RefreshTokenPayload:
        data = self.decode(token)

        return RefreshTokenPayload(
            ident=UUID(data["ident"]),
            user_ident=UUID(data["user_ident"]),
            gen_dt=datetime.strptime(data["gen_dt"], DATETIME_STRING_FORMAT),
            exp_dt=datetime.strptime(data["exp_dt"], DATETIME_STRING_FORMAT),
        )

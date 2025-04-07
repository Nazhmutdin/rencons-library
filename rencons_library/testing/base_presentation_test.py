from uuid import UUID

from pydantic import RootModel
from httpx import AsyncClient, Cookies


class BaseTestEndpoint:

    def _set_access_cookie(self, client: AsyncClient, access_token: str) -> AsyncClient:
        cookies = Cookies()

        cookies["access_token"] = access_token

        client.cookies = cookies


class BaseTestCreateEndpoint[DTO](BaseTestEndpoint):

    async def _test_success_add(self, api_path, item: DTO, client: AsyncClient, access_token: str):
        self._set_access_cookie(client, access_token)

        response = await client.post(api_path, json=RootModel(item).model_dump(mode="json"))

        assert response.status_code == 200
        assert response.text == RootModel(item).model_dump_json(by_alias=True, exclude=["html"])

        return response


    async def _test_failed_add(
        self, 
        api_path, 
        item: DTO, 
        client: AsyncClient, 
        access_token: str, 
        assert_code: int
    ):
        self._set_access_cookie(client, access_token)

        response = await client.post(api_path, json=RootModel(item).model_dump(mode="json", exclude=["html"]))

        assert response.status_code == assert_code

        return response


class BaseTestGetEndpoint[DTO](BaseTestEndpoint):
    __dto__: type[DTO]

    async def _test_success_get(self, api_path, ident: UUID, item: DTO, client: AsyncClient, access_token: str):
        self._set_access_cookie(client, access_token)

        response = await client.get(api_path, params={"ident": ident.hex})

        assert response.status_code == 200
        assert response.text == RootModel(item).model_dump_json(by_alias=True, exclude=["html"])


    async def _test_failed_get(
        self, 
        api_path, 
        ident: UUID, 
        client: AsyncClient, 
        access_token: str, 
        assert_code: int
    ):
        self._set_access_cookie(client, access_token)

        response = await client.get(api_path, params={"ident": ident.hex})

        assert response.status_code == assert_code

        return response


class BaseTestUpdateEndpoint(BaseTestEndpoint):
    __update_shema__: RootModel

    async def _test_success_update(
        self, 
        update_api_path: str, 
        get_api_path: str,
        ident: UUID, 
        data: dict, 
        client: AsyncClient, 
        access_token: str
    ):
        self._set_access_cookie(client, access_token)

        res = await client.patch(
            update_api_path, 
            params={"ident": ident.hex},
            json=self.__update_shema__.model_validate(data).model_dump(mode="json")
        )

        assert res.status_code == 200

        res = await client.get(get_api_path, params={"ident": ident.hex})

        assert res.status_code == 200

        result: dict = self.__update_shema__.model_validate_json(res.text).model_dump(mode="json", by_alias=False)

        for key, value in self.__update_shema__.model_validate(data).model_dump(mode="json", by_alias=False, exclude=["html"]).items():
            assert result[key] == value


    async def _test_failed_update(
        self, 
        api_path: str, 
        ident: UUID, 
        data: dict, 
        client: AsyncClient, 
        access_token: str, 
        assert_code: int
    ):
        self._set_access_cookie(client, access_token)

        response = await client.patch(
            api_path, 
            params={"ident": ident.hex},
            json=data
        )

        assert response.status_code == assert_code

        return response


class BaseTestDeleteEndpoint[DTO](BaseTestEndpoint):

    async def _test_success_delete(
        self, 
        delete_api_path: str, 
        get_api_path: str, 
        create_api_path: str, 
        ident: UUID, 
        item: DTO, 
        client: AsyncClient, 
        access_token: str
    ):
        self._set_access_cookie(client, access_token)

        res = await client.delete(delete_api_path, params={"ident": ident.hex})

        assert res.status_code == 200

        res = await client.get(get_api_path, params={"ident": ident.hex})

        assert res.status_code == 404

        res = await client.post(
            create_api_path, 
            json=RootModel(item).model_dump(mode="json")
        )

        assert res.status_code == 200


    async def _test_failed_delete(
        self, 
        api_path: str, 
        ident: UUID, 
        client: AsyncClient, 
        access_token: str, 
        assert_code: int
    ):
        self._set_access_cookie(client, access_token)

        response = await client.delete(api_path, params={"ident": ident.hex})

        assert response.status_code == assert_code

        return response

from uuid import UUID
from typing import BinaryIO
from pathlib import Path
from hashlib import md5
from os import listdir, remove

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


class BaseTestFileDownloadEndpoint(BaseTestEndpoint):

    async def _test_success(
        self, 
        api_path: str,
        file: BinaryIO,
        client: AsyncClient, 
        access_token: str
    ): 
        self._set_access_cookie(client, access_token)

        response = await client.get(api_path)

        response_checksum = self.compute_checksum(response.content)
        file_checksum = self.compute_checksum(file.read())

        assert response.status_code == 200
        assert response_checksum == file_checksum

        return response


    async def _test_failed(
        self, 
        api_path: str, 
        client: AsyncClient, 
        access_token: str, 
        assert_code: int
    ): 
        self._set_access_cookie(client, access_token)
        
        response = await client.get(api_path)

        assert response.status_code == assert_code

        return response


    def compute_checksum(self, data: str | bytes) -> str:
        return md5(data).hexdigest()


class BaseTestFileUploadEndpoint(BaseTestEndpoint):

    async def _test_success(
        self, 
        api_path: str,
        file: BinaryIO,
        static_folder_path: Path,
        client: AsyncClient, 
        access_token: str
    ): 
        self._set_access_cookie(client, access_token)
        before_files_amount = len(listdir(static_folder_path))

        response = await client.post(
            api_path,
            files={
                "file": file
            }
        )
        
        after_files_amount = len(listdir(static_folder_path))

        assert response.status_code == 200
        assert (after_files_amount - before_files_amount) == 1

        for file_name in listdir(static_folder_path):
            remove(static_folder_path / file_name)

        return response


    async def _test_failed(
        self, 
        api_path: str,
        file: BinaryIO,
        client: AsyncClient, 
        access_token: str,
        assert_code: int
    ): 
        self._set_access_cookie(client, access_token)

        response = await client.post(
            api_path,
            files={
                "file": file
            }
        )

        assert response.status_code == assert_code

        return response

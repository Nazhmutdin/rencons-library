import typing as t
from uuid import UUID, uuid4
from datetime import datetime, date

from pydantic import BaseModel

from rencons_library.utils.validators import (
    before_date_validator,
    plain_date_serializer,
    before_optional_date_validator,
    before_datetime_validator,
    plain_datetime_serializer,
    before_optional_datetime_validator,
    before_uuid_validator, 
    before_optional_uuid_validator,
    plain_optional_date_serializer,
    plain_optional_datetime_serializer,
    plain_uuid_serializer,
    plain_optional_uuid_serializer
)
from rencons_library import DATE_STRING_FORMAT, DATETIME_STRING_FORMAT


class PydanticTestModel(BaseModel):
    a_field: t.Annotated[date, before_date_validator, plain_date_serializer]
    b_field: t.Annotated[date | None, before_optional_date_validator, plain_optional_date_serializer]
    c_field: t.Annotated[datetime, before_datetime_validator, plain_datetime_serializer]
    d_field: t.Annotated[datetime | None, before_optional_datetime_validator, plain_optional_datetime_serializer]
    e_field: t.Annotated[UUID, before_uuid_validator, plain_uuid_serializer]
    f_field: t.Annotated[UUID | None, before_optional_uuid_validator, plain_optional_uuid_serializer]


class TestPydanticValidators:
    data1 = {
        "a_field": date.today(),
        "b_field": date.today(),
        "c_field": datetime.now(),
        "d_field": datetime.now(),
        "e_field": uuid4(),
        "f_field": uuid4()
    }
    data2 = {
        "a_field": date.today(),
        "b_field": None,
        "c_field": datetime.now(),
        "d_field": None,
        "e_field": uuid4(),
        "f_field": None
    }


    def test_date_validators_and_serializers(self):
        model1 = PydanticTestModel.model_validate(self.data1).model_dump(mode="json")
        model2 = PydanticTestModel.model_validate(self.data2).model_dump(mode="json")

        assert model1["a_field"] == date.strftime(self.data1["a_field"], DATE_STRING_FORMAT)

        assert model1["b_field"] == date.strftime(self.data1["b_field"], DATE_STRING_FORMAT)

        assert model2["b_field"] is None


    def test_datetime_validators_and_serializers(self):
        model1 = PydanticTestModel.model_validate(self.data1).model_dump(mode="json")
        model2 = PydanticTestModel.model_validate(self.data2).model_dump(mode="json")

        assert model1["c_field"] == datetime.strftime(self.data1["c_field"], DATETIME_STRING_FORMAT)

        assert model1["d_field"] == datetime.strftime(self.data1["d_field"], DATETIME_STRING_FORMAT)

        assert model2["d_field"] is None


    def test_uuid_validators_and_serializers(self):
        model1 = PydanticTestModel.model_validate(self.data1).model_dump(mode="json")
        model2 = PydanticTestModel.model_validate(self.data2).model_dump(mode="json")

        assert model1["e_field"] == str(self.data1["e_field"])
        assert UUID(model1["e_field"]) == self.data1["e_field"]

        assert model1["e_field"] == str(self.data1["e_field"])
        assert UUID(model1["e_field"]) == self.data1["e_field"]

        assert model2["f_field"] is None

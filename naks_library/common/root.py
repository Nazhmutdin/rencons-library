from pydantic import BaseModel, ConfigDict, AliasGenerator, Field

from naks_library.utils.funcs import from_snake_case_to_lower_camel_case


camel_case_serialization_alias_generator = AliasGenerator(serialization_alias=from_snake_case_to_lower_camel_case)


class BaseShema(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        validate_assignment=True,
        revalidate_instances="always",
        alias_generator=camel_case_serialization_alias_generator
    )


class BaseSelectShema(BaseShema):
    limit: int = Field(default=100)
    offset: int = Field(default=0)

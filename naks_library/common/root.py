from pydantic import BaseModel, ConfigDict, AliasGenerator, Field
from pydantic.alias_generators import to_camel


camel_case_alias_generator = AliasGenerator(alias=to_camel)


class BaseShema(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        validate_assignment=True,
        revalidate_instances="always",
        alias_generator=camel_case_alias_generator
    )


class BaseSelectShema(BaseShema):
    limit: int = Field(default=100)
    offset: int = Field(default=0)

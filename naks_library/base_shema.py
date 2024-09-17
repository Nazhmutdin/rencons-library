from pydantic import BaseModel, ConfigDict, Field


class BaseShema(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        validate_assignment=True,
        revalidate_instances="always",
    )


class BaseSelectShema(BaseShema):
    limit: int = Field(default=100)
    offset: int = Field(default=0)

import typing as t
from collections.abc import AsyncGenerator

from datetime import date, timedelta
from os import getenv
import uuid

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, InstrumentedAttribute, join
import sqlalchemy as sa

from pydantic.dataclasses import dataclass
from pydantic import BaseModel, Field

from faker import Faker

from naks_library import Eq
from naks_library.crud_mapper import SqlAlchemyCrudMapper
from naks_library.utils.funcs import seq
from naks_library import BaseShema
from naks_library.selector_filters import AbstractFilter, EqualFilter, ILikeAnyFilter, ILikeFilter, InFilter, FromFilter, BeforeFilter, LikeFilter, LikeAnyFilter
from naks_library.interactors import BaseGetInteractor, BaseCreateInteractor, BaseDeleteInteractor, BaseUpdateInteractor


DB_URL = "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(
    getenv("USER"), 
    getenv("DATABASE_PASSWORD"), 
    getenv("HOST"), 
    getenv("PORT"), 
    getenv("DATABASE_NAME")
)


STRINGS = [
    "string1",
    "string2",
    "string3",
    "string4",
    "string5",
    "string6",
    "string7",
    "string8",
    "string9"
]


engine = create_async_engine(
    DB_URL,
    poolclass=sa.NullPool
)

session_maker = async_sessionmaker(engine, autocommit=False, autoflush=False, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session


class ADict(t.TypedDict): 
    ident: uuid.UUID
    foo1: float
    foo2: str
    foo3: date
    foo4: date
    foo5: float
    foo6: str


class BDict(t.TypedDict): 
    ident: uuid.UUID
    a_ident: uuid.UUID
    foo1: float
    foo2: str
    foo3: date
    foo4: date
    foo5: float
    foo6: list[str]


@dataclass(eq=False)
class AData(Eq): 
    ident: uuid.UUID
    foo1: float
    foo2: str
    foo3: date
    foo4: date
    foo5: float
    foo6: str


@dataclass(eq=False)
class BData(Eq): 
    ident: uuid.UUID
    a_ident: uuid.UUID
    foo1: float
    foo2: str
    foo3: date
    foo4: date
    foo5: float
    foo6: list[str]


class Base(DeclarativeBase): ...


class AModel(Base):
    __tablename__ = "a_table"

    ident: Mapped[uuid.UUID] = sa.Column(sa.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    foo1: Mapped[float] = sa.Column(sa.Float)
    foo2: Mapped[str] = sa.Column(sa.String)
    foo3: Mapped[date] = sa.Column(sa.Date)
    foo4: Mapped[date] = sa.Column(sa.Date)
    foo5: Mapped[float] = sa.Column(sa.Float)
    foo6: Mapped[str] = sa.Column(sa.String())


class BModel(Base):
    __tablename__ = "b_table"

    ident: Mapped[uuid.UUID] = sa.Column(sa.UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    a_ident: Mapped[uuid.UUID] = sa.Column(sa.UUID(as_uuid=True), sa.ForeignKey("a_table.ident", ondelete="CASCADE", onupdate="CASCADE"))
    foo1: Mapped[float] = sa.Column(sa.Float)
    foo2: Mapped[str] = sa.Column(sa.String)
    foo3: Mapped[date] = sa.Column(sa.Date)
    foo4: Mapped[date] = sa.Column(sa.Date)
    foo5: Mapped[float] = sa.Column(sa.Float)
    foo6: Mapped[list[str]] = sa.Column(sa.ARRAY(sa.String))


B_FILTERS_MAP: dict[str, AbstractFilter] = {
    "idents": InFilter(BModel.ident),
    "a_idents": InFilter(BModel.a_ident),
    "foo1_from": FromFilter(BModel.foo1),
    "foo1_before": BeforeFilter(BModel.foo1),
    "foo2": EqualFilter(BModel.foo2),
    "foo3_from": FromFilter(BModel.foo3),
    "foo3_before": BeforeFilter(BModel.foo3),
    "foo4_from": FromFilter(BModel.foo4),
    "foo4_before": BeforeFilter(BModel.foo4),
    "foo5_from": FromFilter(BModel.foo5),
    "foo5_before": BeforeFilter(BModel.foo5),
    "foo6": ILikeAnyFilter(BModel.foo6),
}

B_SELECT_ATTRS = [
    BModel
]


B_SELECT_FROM_ATTRS = [
    BModel
]

B_OR_SELECT_COLUMNS: list[InstrumentedAttribute] = [
    BModel.ident,
    BModel.a_ident
]


B_AND_SELECT_COLUMNS: list[InstrumentedAttribute] = [
    BModel.foo1,
    BModel.foo2,
    BModel.foo3,
    BModel.foo4,
    BModel.foo5,
    BModel.foo6
]


A_FILTERS_MAP: dict[str, AbstractFilter] = {
    "idents": InFilter(AModel.ident),
    "foo1_from": FromFilter(AModel.foo1),
    "foo1_before": BeforeFilter(AModel.foo1),
    "foo2": EqualFilter(AModel.foo2),
    "foo3_from": FromFilter(AModel.foo3),
    "foo3_before": BeforeFilter(AModel.foo3),
    "foo4_from": FromFilter(AModel.foo4),
    "foo4_before": BeforeFilter(AModel.foo4),
    "foo5_from": FromFilter(AModel.foo5),
    "foo5_before": BeforeFilter(AModel.foo5),
    "foo6": ILikeFilter(AModel.foo6),
    "b_idents": InFilter(BModel.ident),
    "b_foo1_from": FromFilter(BModel.foo1),
    "b_foo1_before": BeforeFilter(BModel.foo1),
    "b_foo2": EqualFilter(BModel.foo2),
    "b_foo3_from": FromFilter(BModel.foo3),
    "b_foo3_before": BeforeFilter(BModel.foo3),
    "b_foo4_from": FromFilter(BModel.foo4),
    "b_foo4_before": BeforeFilter(BModel.foo4),
    "b_foo5_from": FromFilter(BModel.foo5),
    "b_foo5_before": BeforeFilter(BModel.foo5),
    "b_foo6": ILikeAnyFilter(BModel.foo6),
}


A_SELECT_ATTRS = [
    AModel
]


A_SELECT_FROM_ATTRS = [
    join(AModel, BModel)
]


A_OR_SELECT_COLUMNS: list[InstrumentedAttribute] = [
    BModel.ident,
    AModel.ident
]


A_AND_SELECT_COLUMNS: list[InstrumentedAttribute] = [
    BModel.foo1,
    BModel.foo2,
    BModel.foo3,
    BModel.foo4,
    BModel.foo5,
    BModel.foo6,
    AModel.foo1,
    AModel.foo2,
    AModel.foo3,
    AModel.foo4,
    AModel.foo5,
    AModel.foo6
]


class CreateAShema(BaseModel):
    ident: uuid.UUID
    foo1: float
    foo2: str
    foo3: date
    foo4: date
    foo5: float
    foo6: str


class UpdateAShema(BaseModel):
    ident: uuid.UUID | None = Field(default=None)
    foo1: float | None = Field(default=None)
    foo2: str | None = Field(default=None)
    foo3: date | None = Field(default=None)
    foo4: date | None = Field(default=None)
    foo5: float | None = Field(default=None)
    foo6: str | None = Field(default=None)

@dataclass
class CreateADTO:
    ident: uuid.UUID
    foo1: float
    foo2: str
    foo3: date
    foo4: date
    foo5: float
    foo6: str


@dataclass
class UpdateADTO:
    foo1: float | None
    foo2: str | None
    foo3: date | None
    foo4: date | None
    foo5: float | None
    foo6: str | None


class SelectAShema(BaseShema):
    idents: list[uuid.UUID] | None = Field(default=None)
    foo1_from: float | None = Field(default=None)
    foo1_before: float | None = Field(default=None)
    foo2: str | None = Field(default=None)
    foo3_from: date | None = Field(default=None)
    foo3_before: date | None = Field(default=None)
    foo4_from: date | None = Field(default=None)
    foo4_before: date | None = Field(default=None)
    foo5_from: float | None = Field(default=None)
    foo5_before: float | None = Field(default=None)
    foo6: list[str] | None = Field(default=None)
    b_idents: list[uuid.UUID] | None = Field(default=None)
    b_foo1_from: float | None = Field(default=None)
    b_foo1_before: float | None = Field(default=None)
    b_foo2: str | None = Field(default=None)
    b_foo3_from: date | None = Field(default=None)
    b_foo3_before: date | None = Field(default=None)
    b_foo4_from: date | None = Field(default=None)
    b_foo4_before: date | None = Field(default=None)
    b_foo5_from: float | None = Field(default=None)
    b_foo5_before: float | None = Field(default=None)
    b_foo6: list[str] | None = Field(default=None)


def filter_data[DTO](filters: SelectAShema, all_data: list[DTO]) -> list[DTO]:

    mode = "a" if isinstance(filters, SelectAShema) else "b"

    filters_map = A_FILTERS_MAP if mode == "a" else B_FILTERS_MAP

    for key, filter_arg in filters.model_dump(exclude_none=True, exclude_unset=True).items():
        map_arg = filters_map[key]

        if isinstance(map_arg, FromFilter):
            all_data = [el for el in all_data if getattr(el, map_arg.column.key) > filter_arg]

        if isinstance(map_arg, BeforeFilter):
            all_data = [el for el in all_data if getattr(el, map_arg.column.key) < filter_arg]

        if isinstance(map_arg, InFilter):
            all_data = [el for el in all_data if getattr(el, map_arg.column.key) in filter_arg]

        if isinstance(map_arg, EqualFilter):
            all_data = [el for el in all_data if getattr(el, map_arg.column.key) == filter_arg]

        if isinstance(map_arg, LikeFilter):
            all_data = [el for el in all_data if filter_arg in getattr(el, map_arg.column.key)]

        if isinstance(map_arg, ILikeFilter):
            all_data = [el for el in all_data if filter_arg in str.lower(getattr(el, map_arg.column.key))]

        if isinstance(map_arg, LikeAnyFilter):
            all_data = [el for el in all_data if any([filter_arg in filt for filt in getattr(el, map_arg.column.key)])]

        if isinstance(map_arg, ILikeAnyFilter):
            all_data = [el for el in all_data if filter_arg in str.lower(getattr(el, map_arg.column.key))]


class ACrudMapper(SqlAlchemyCrudMapper[AData, CreateADTO, UpdateADTO]):
    __model__ = AModel

    def _convert(self, row: sa.Row[t.Any]) -> AData:
        return AData(**row.__dict__)
    

class GetAInteractor(BaseGetInteractor): ...
class CreateAInteractor(BaseCreateInteractor): ...
class UpdateAInteractor(BaseUpdateInteractor): ...
class DeleteAInteractor(BaseDeleteInteractor): ...


class BaseFakeDataGenerator[T]:
    faker = Faker()

    def generate() -> list[T]: ...


    def gen_random_date(self, start: date, end: date) -> date:
        return self.faker.date_between(start, end)


    def gen_random_float(self, start: float, end: float, step: float) -> float:
        return self.faker.random_element(seq(start, end, step))


class FakeADataGenerator(BaseFakeDataGenerator):
    faker = Faker()

    def generate(self, k: int = 100) -> list[ADict]:
        data = []

        for _ in range(k):
            sub_data: ADict = {}

            sub_data["ident"] = uuid.uuid4()
            sub_data["foo1"] = self.gen_random_float(0, 5000, 0.1)
            sub_data["foo2"] = self.faker.random_element(STRINGS)
            sub_data["foo3"] = self.gen_random_date(
                date.today() - timedelta(weeks=100),
                date.today()
            )
            sub_data["foo4"] = self.faker.date_between(
                date.today() - timedelta(weeks=100),
                date.today()
            )
            sub_data["foo5"] = self.gen_random_float(0, 5000, 0.1)
            sub_data["foo6"] = self.faker.random_element(STRINGS)

            data.append(sub_data)
        
        return data


class FakeBDataGenerator(BaseFakeDataGenerator):
    faker = Faker()

    def __init__(self, a_data: list[AData]) -> None:
        self.a_data = a_data


    def generate(self, k: int = 100) -> list[BDict]:
        data = []

        for _ in range(k):
            sub_data: BDict = {}

            sub_data["ident"] = uuid.uuid4()
            sub_data["a_ident"] = self.faker.random_element(self.a_data).ident
            sub_data["foo1"] = self.gen_random_float(0, 5000, 0.1)
            sub_data["foo2"] = self.faker.random_element(STRINGS)
            sub_data["foo3"] = self.gen_random_date(
                date.today() - timedelta(weeks=100),
                date.today()
            )
            sub_data["foo4"] = self.gen_random_date(
                date.today() - timedelta(weeks=100),
                date.today()
            )
            sub_data["foo5"] = self.gen_random_float(0, 5000, 0.1)
            sub_data["foo6"] = list(self.faker.random_elements(STRINGS))

            data.append(sub_data)
        
        return data


class TestData: 
    faker = Faker()
    def __init__(self) -> None:
        self.fake_a_generator = FakeADataGenerator()
        self.fake_a_dicts = self.fake_a_generator.generate(10)
        self.fake_a = [AData(**el) for el in self.fake_a_dicts]
        self.fake_b_generator = FakeBDataGenerator(self.fake_a)
        self.fake_b_dicts = self.fake_b_generator.generate(50)
        self.fake_b = [BData(**el) for el in self.fake_b_dicts]


    def get_random_a(self):
        return self.faker.random_element(self.fake_a)

    
    def get_random_a_ident(self) -> uuid.UUID:
        return self.get_random_a().ident


    def get_random_b(self):
        return self.faker.random_element(self.fake_b)

    
    def get_random_b_ident(self) -> uuid.UUID:
        return self.get_random_b().ident

    
    def get_random_b_a_ident(self) -> uuid.UUID:
        return self.faker.random_element(self.fake_b).a_ident


    def get_random_a_idents(self, k: int = 5) -> list[uuid.UUID]:
        return [self.get_random_a_ident() for _ in range(k)]


    def get_random_b_idents(self, k: int = 5) -> list[uuid.UUID]:
        return [self.get_random_b_ident() for _ in range(k)]


    def get_random_b_a_idents(self, k: int = 5) -> list[uuid.UUID]:
        return [self.get_random_b_a_ident() for _ in range(k)]
    

    def get_a_by_ident(self, ident: uuid.UUID) -> AData:
        for a in self.fake_a:
            if a.ident == ident:
                return a
    

    def get_b_by_ident(self, ident: uuid.UUID) -> BData:
        for b in self.fake_b:
            if b.ident == ident:
                return b


test_data = TestData()

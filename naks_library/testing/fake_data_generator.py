from datetime import date

from faker import Faker

from naks_library.funcs import seq


class BaseFakeDataGenerator[T]:
    faker = Faker()

    def generate() -> list[T]: ...


    def gen_random_date(self, start: date, end: date) -> date:
        return self.faker.date_between(start, end)


    def gen_random_float(self, start: float, end: float, step: float) -> float:
        return self.faker.random_element(seq(start, end, step))

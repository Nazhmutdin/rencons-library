from naks_library.commiter import ICommitter, SqlAlchemyCommitter
from naks_library.crud_mapper import ICrudMapper, SqlAlchemySessionInitializer, SqlAlchemyCrudMapper


DATE_STRING_FORMAT = "%d.%m.%Y"
DATETIME_STRING_FORMAT = "%d.%m.%Y %H:%M:%S.%f%z"


class Eq:
    def __eq__(self, other) -> bool:
        self_dict = self.__dict__

        for key, value in other.__dict__.items():
            if self_dict[key] != value:
                return False
            
        return True

from naks_library.base_shema import BaseShema
from naks_library.funcs import *
from naks_library.base_db_service import BaseDBService


class Eq:
    def __eq__(self, other) -> bool:
        self_dict = self.__dict__

        for key, value in other.__dict__.items():
            if self_dict[key] != value:
                return False
            
        return True

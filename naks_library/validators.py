from re import fullmatch
from uuid import UUID


__all__ = [
    "is_kleymo",
    "is_uuid",
    "is_float"
]


def is_kleymo(v: str) -> bool:
    if fullmatch(r"[A-Z0-9]{4}", v):
        return True
    
    return False


def is_uuid(uuid: str | UUID) -> True:
    try:
        UUID(uuid)
        return True
    except:
        return False


def is_float(v: str) -> bool:
    try:
        float(v)
        return True
    except:
        return False

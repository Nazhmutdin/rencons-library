from uuid import UUID
from re import fullmatch


__all__ = [
    "seq",
    "to_uuid",
    "is_float",
    "is_kleymo",
    "is_uuid",
]

def seq(start: int, stop: int, step: float | int):
    result = []
    cur = start

    if start > stop:
        raise ValueError
    
    if step <= 0:
        raise ValueError

    while cur < stop:
        result.append(cur)
        cur += step

    return result


def is_float(v: str) -> bool:
    try:
        float(v)
        return True
    except:
        return False


def is_kleymo(v: str) -> bool:
    if fullmatch(r"[A-Z0-9]{4}", v):
        return True
    
    return False


def is_uuid(uuid: str | UUID) -> bool:
    if isinstance(uuid, UUID):
        return True
    
    try:
        UUID(uuid)
        return True
    except:
        return False


def to_uuid(v: str | UUID) -> UUID:
    if isinstance(v, UUID):
        return v
    
    return UUID(v)


def from_snake_case_to_lower_camel_case(string: str) -> str:
    upper = "".join(word.capitalize() for word in string.split("_"))
    return upper[:1].lower() + upper[1:]

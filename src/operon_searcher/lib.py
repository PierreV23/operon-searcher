import dataclasses
from enum import Enum
import inspect
from typing import Callable

# `str` is nodig om dit object json serializable te maken.
class Strand(str, Enum):
    Positive = '+'
    Negative = '-'


def automatic_field_converter(self):  # Credit: https://stackoverflow.com/a/54863733
    for field in dataclasses.fields(self):
        value = getattr(self, field.name)
        # if not isinstance(field.default, dataclasses._MISSING_TYPE) and getattr(self, field.name) is None:
        #         setattr(self, field.name, field.default)
        if not isinstance(value, field.type):
            try:
                self.__dict__[field.name] = field.type(value)
            except:
                raise ValueError(f'Expected {field.name} to be {field.type}, got {repr(value)}')
            # raise ValueError(f'Expected {field.name} to be {field.type}, got {repr(value)}')
            # or setattr(self, field.name, field.type(value))

@classmethod
def from_dict(cls, env):  # Credits: https://stackoverflow.com/a/55096964
    return cls(**{
        k: v for k, v in env.items() 
        if k in inspect.signature(cls).parameters
    })

def parse_rest(txt) -> dict[str, str]:
    data = {}
    for var in txt.split(";"):
        if '=' not in var:
            # print(var)
            continue
        var_name, var_value = var.split("=")
        data[var_name.lower()] = var_value.strip("\n")
    return data

@dataclasses.dataclass
class SubSequence(): # Misschien dit singleton maken?
    organism_id: str
    start: int
    end: int
    strand: Strand
    __post_init__ = automatic_field_converter

    def __hash__(self) -> int:
        return str.__hash__(f"{self.organism_id}-{self.start}-{self.end}-{self.strand.value}")


def timer(func: Callable):
    print(f"{func.__name__} INIT")
    def inner(*args, **kwargs):
        print(f"{func.__name__} STARTING")
        r=func(*args, **kwargs)
        print(f"{func.__name__} DONE")
        return r
    return inner
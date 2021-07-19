from typing import NamedTuple
from itertools import product

class Source(NamedTuple):
    src: str
    span: str

class Action(NamedTuple):
    srcs: tuple
    dst: str
    type: str


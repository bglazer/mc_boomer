from typing import NamedTuple

class Source(NamedTuple):
    src: str

class MultiSource(NamedTuple):
    src: str
    span: str

class Action(NamedTuple):
    srcs: tuple
    dst: str
    type: str


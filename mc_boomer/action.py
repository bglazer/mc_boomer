from typing import NamedTuple

class Source(NamedTuple):
    src: str
    neg: bool = False

class MultiSource(NamedTuple):
    src: str
    span: str
    neg: bool = False

class Node(NamedTuple):
    src: str
    neg: bool = False
    def __hash__(self):
        return hash(self.src)
    def __eq__(self,other):
        return self.src==other

class MultiNode(NamedTuple):
    src: str
    idx: int
    neg: bool = False
    def __hash__(self):
        return hash((self.src,self.idx))
    def __eq__(self, other):
        return (self.src, self.idx) == other

class Action(NamedTuple):
    srcs: tuple
    dst: str
    type: str


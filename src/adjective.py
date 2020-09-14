
from typing import Optional

from term import Term

class Adjective(Term):
    def __init__(self, term: str, classical:Optional[bool] = False):
        super().__init__(term, classical)

    """
    Override default methods from Term    
    """
    def is_adj(self) -> bool:
        return True

    def is_singular(self) -> bool:
        raise NotImplementedError()

    def is_plural(self) -> bool:
        raise NotImplementedError()

    def singular(self, person:Optional[int] = 0) -> str:
        raise NotImplementedError()

    def plural(self, person:Optional[int] = 0) -> str:
        raise NotImplementedError()
    
    def as_regex(self) -> str:
        raise NotImplementedError()

if __name__ == "__main__":
    a = Adjective("typical")
    breakpoint()
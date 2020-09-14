
from typing import Optional

from term import Term

class Adjective(Term):
    def __init__(self, adjective):
        super().__init__()
        self.adjective = adjective

    """
    Override default methods from Term    
    """
    def is_adjective(self) -> bool:
        return True

    def is_singular(self) -> bool:
        raise NotImplementedError()

    def is_plural(self) -> bool:
        raise NotImplementedError()

    def singular(self, person:Optional[int] = None) -> str:
        raise NotImplementedError()

    def plural(self, person:Optional[int] = None) -> str:
        raise NotImplementedError()

    def classical(self) -> "Term":
        raise NotImplementedError()

    def unassimilated(self) -> "Term":
        return self.classical()
    
    def as_regex(self) -> str:
        raise NotImplementedError()

if __name__ == "__main__":
    a = Adjective("typical")
    breakpoint()

from typing import Optional

from term import Term

class Verb(Term):
    def __init__(self, verb):
        super().__init__()
        self.verb = verb

    """
    Override default methods from Term    
    """
    def is_verb(self) -> bool:
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

    """
    Methods exclusively for Verb
    """
    def past(self) -> str:
        raise NotImplementedError()

    def pres_part(self) -> str:
        raise NotImplementedError()

    def past_part(self) -> str:
        raise NotImplementedError()
    
    def is_present(self) -> str:
        raise NotImplementedError()
    
    def is_past(self) -> str:
        raise NotImplementedError()

    def is_pres_part(self) -> str:
        raise NotImplementedError()

    def is_past_part(self) -> str:
        raise NotImplementedError()

    def indefinite(self, count: int) -> str:
        raise NotImplementedError()

if __name__ == "__main__":
    v = Verb("slap")
    breakpoint()
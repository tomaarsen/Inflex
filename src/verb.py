
from typing import Optional

from term import Term
from verb_core import (
    is_plural,
    is_singular,
    #is_present,
    is_past,
    is_pres_part,
    is_past_part,
)

class Verb(Term):
    def __init__(self, term: str, classical:Optional[bool] = False):
        super().__init__(term, classical)

    """
    Override default methods from Term    
    """
    def is_verb(self) -> bool:
        return True

    def is_singular(self) -> bool:
        return is_singular(self.term)

    def is_plural(self) -> bool:
        return is_plural(self.term)

    def singular(self, person:Optional[int] = 0) -> str:
        raise NotImplementedError()

    def plural(self, person:Optional[int] = 0) -> str:
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
        # TODO: Does not exist
        #is_present(self.term)
        raise NotImplementedError()
    
    def is_past(self) -> str:
        is_past(self.term)

    def is_pres_part(self) -> str:
        is_pres_part(self.term)

    def is_past_part(self) -> str:
        is_past_part(self.term)

    def indefinite(self, count: int) -> str:
        raise NotImplementedError()

if __name__ == "__main__":
    v = Verb("slap")
    breakpoint()
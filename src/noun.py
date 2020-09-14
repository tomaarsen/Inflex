
from typing import Optional

from term import Term
from noun_core import is_singular,\
                      is_plural,\
                      convert_to_classical_plural,\
                      convert_to_modern_plural,\
                      convert_to_singular

class Noun(Term):
    def __init__(self, term: str, classical:Optional[bool] = False):
        super().__init__(term, classical)

    """
    Override default methods from Term    
    """
    def is_noun(self) -> bool:
        return True

    def is_singular(self) -> bool:
        return is_singular(self.noun)

    def is_plural(self) -> bool:
        return is_plural(self.noun)

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
    Methods exclusively for Noun
    """
    def indef_article(self) -> str:
        raise NotImplementedError()

    def indefinite(self, count: int) -> str:
        raise NotImplementedError()
    
    def cardinal(self, threshold: int) -> str:
        raise NotImplementedError()
    
    def ordinal(self, threshold: int) -> str:
        raise NotImplementedError()

if __name__ == "__main__":
    n = Noun("fish")
    breakpoint()
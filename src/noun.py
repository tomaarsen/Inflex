
from typing import Optional

from term import Term

class Noun(Term):
    def __init__(self, noun):
        super().__init__()
        self.noun = noun

    """
    Override default methods from Term    
    """
    def is_noun(self) -> bool:
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
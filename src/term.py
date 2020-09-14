
from typing import Optional

class Term(object):
    def __init__(self):
        super().__init__()

    def is_noun(self) -> bool:
        return False

    def is_verb(self) -> bool:
        return False

    def is_adj(self) -> bool:
        return False

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
    breakpoint()
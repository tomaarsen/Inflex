#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional

class Term(object):
    def __init__(self, term: str):
        super().__init__()
        self.term = term

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

    def singular(self, person:Optional[int] = 0) -> str:
        # TODO: Implement bound call on person
        raise NotImplementedError()

    def plural(self, person:Optional[int] = 0) -> str:
        # TODO: Implement bound call on person
        raise NotImplementedError()

    def classical(self) -> "Term":
        return self

    def unassimilated(self) -> "Term":
        return self.classical()
    
    def as_regex(self) -> str:
        return "|".join(dict.fromkeys((self.singular(),
                                       self.plural(),
                                       self.classical().plural())))

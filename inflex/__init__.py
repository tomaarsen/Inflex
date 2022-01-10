"""
Import the Noun, Verb and Adjective classes from the relevant files,
allowing for::

    >>> from inflex import Noun, Verb, Adjective
"""
__all__ = [
    "Noun",
    "Verb",
    "Adjective",
]

from inflex.noun import Noun
from inflex.verb import Verb
from inflex.adjective import Adjective

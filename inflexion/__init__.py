"""
Import the Noun, Verb and Adjective classes from the relevant files,
allowing for:
>>> from inflexion import Noun
"""
__all__ = [
    "Noun",
    "Verb",
    "Adjective",
]

from inflexion.noun import Noun
from inflexion.verb import Verb
from inflexion.adjective import Adjective

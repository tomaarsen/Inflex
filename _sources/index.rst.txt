
Inflex
======

The Inflex module is a rule-based morphological analyser and generator.
It allows for conversions of any noun, verb or adjective to a specific wordform such as singular, plural, past, past participle or present participle.

Inflex can be tried out and compared against competitors including ``nltk``, ``textblob``, ``pattern``, ``inflect``, ``inflection``, ``inflector``, ``lemminflect``, and ``pyinflect`` on https://www.tomaarsen.com/projects/inflex/try.
Furthermore, the comparison of performance of all of these modules is visualised on https://www.tomaarsen.com/projects/inflex/performance, using several different datasets.
These results show that Inflex outperforms all existing modules for noun conversions, and performs competitively for verbs.
This website also contains the thesis out of which Inflex (formerly called Inflexion) was born.

Sample usage
++++++++++++

.. code-block:: Python

   from inflex import Noun, Verb, Adjective

   # Converting Nouns
   Noun("book").plural()   # Produces "books"
   Noun("book").singular() # Produces "book"

   # Converting Verbs
   Verb("fly").plural()    # Produces "fly"
   Verb("fly").singular()  # Produces "flies"
   Verb("fly").past()      # Produces "flew"
   Verb("fly").pres_part() # Produces "flying"
   Verb("fly").past_part() # Produces "flown"

   # Converting Adjectives
   Adjective("my").singular()       # Produces "my"
   Adjective("our").plural()        # Produces "our"
   Adjective("small").comparative() # Produces "smallest"
   Adjective("small").superlative() # Produces "smaller"

See `Quick Reference </reference.html>`_ for a brief reference of Inflex, or `API Reference </api/inflex.html>`_ for the full API Reference.

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Inflex
   :titlesonly:

   Home <self>
   API Reference <api/inflex>
   Quick Reference <reference>
   Module Index <py-modindex>
   GitHub <https://github.com/tomaarsen/Inflex>

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Installation

   install

.. _API Reference: api/inflex.html


Example Usage
=============

Quick Reference
+++++++++++++++

Inflex provides three objects, which contain the following most important methods: 

:`Noun`_: 

    Let's introduce a running example:

        >>> noun = Noun("brother")

    * `singular </api/inflex.noun.html#inflex.noun.Noun.singular>`_: Return the singular form of this noun.

        >>> noun.singular()
        "brother"

    * `plural </api/inflex.noun.html#inflex.noun.Noun.plural>`_: Return the plural form of this noun.

        >>> noun.plural()
        "brothers"

    * `lemma </api/inflex.noun.html#inflex.noun.Noun.lemma>`_: Return the lemma for this noun, identical to `singular </api/inflex.noun.html#inflex.noun.Noun.singular>`_.
    * `is_singular </api/inflex.noun.html#inflex.noun.Noun.is_singular>`_: Return whether this noun is singular.

        >>> noun.is_singular()
        True

    * `is_plural </api/inflex.noun.html#inflex.noun.Noun.is_plural>`_: Return whether this noun is plural.

        >>> noun.is_plural()
        False

    * `classical </api/inflex.noun.html#inflex.noun.Noun.classical>`_ / `unassimilated </api/inflex.noun.html#inflex.noun.Noun.unassimilated>`_: Return a `ClassicalNoun </api/inflex.noun.html#inflex.noun.ClassicalNoun>`_ instance, which is a subclass of `Noun`_, but with classical conversions instead.

        >>> noun.classical().plural()
        "brethren"

    * `as_regex </api/inflex.noun.html#inflex.noun.Noun.as_regex>`_: Return a re.Pattern which matches any inflected form of the word.

        >>> noun.as_regex()
        re.compile('brothers|brother|brethren', re.IGNORECASE)

    * `indef_article </api/inflex.noun.html#inflex.noun.Noun.indef_article>`_: Return the correct indefinite article ('a' or 'an') for word.

        >>> noun.indef_article()
        "a"

    * `indefinite </api/inflex.noun.html#inflex.noun.Noun.indefinite>`_: Prepend 'a' or 'an' or the number to the correct form of this Noun.
    
        >>> noun.indefinite(count = 1)
        "a brother"
        >>> noun.indefinite(count = 3)
        '3 brothers'

:`Verb`_:

    Let's introduce a running example:

        >>> verb = Verb("fly")

    * `singular </api/inflex.verb.html#inflex.verb.Verb.singular>`_: Return the singular form of this verb.

        >>> verb.singular()
        "flies"

    * `plural </api/inflex.verb.html#inflex.verb.Verb.plural>`_: Return the plural form of this verb.

        >>> verb.plural()
        "fly"

    * `past </api/inflex.verb.html#inflex.verb.Verb.past>`_: Return the past form of this verb.

        >>> verb.past()
        "flew"

    * `pres_part </api/inflex.verb.html#inflex.verb.Verb.pres_part>`_: Return the present participle form of this verb.

        >>> verb.pres_part()
        "flying"

    * `past_part </api/inflex.verb.html#inflex.verb.Verb.past_part>`_: Return the past participle form of this verb.

        >>> verb.past_part()
        "flown"

    * `lemma </api/inflex.verb.html#inflex.verb.Verb.lemma>`_: Return the lemma for this noun, identical to `plural </api/inflex.verb.html#inflex.verb.Verb.plural>`_.
    * `is_singular </api/inflex.verb.html#inflex.verb.Verb.is_singular>`_: Return whether this verb is in singular form.

        >>> verb.is_singular()
        False

    * `is_plural </api/inflex.verb.html#inflex.verb.Verb.is_plural>`_: Return whether this verb is in plural form.

        >>> verb.is_plural()
        True

    * `is_past </api/inflex.verb.html#inflex.verb.Verb.is_past>`_: Return whether this verb is in past form.

        >>> verb.is_past()
        False

    * `is_pres_part </api/inflex.verb.html#inflex.verb.Verb.is_pres_part>`_: Return whether this verb is in present participle form.

        >>> verb.is_pres_part()
        False

    * `is_past_part </api/inflex.verb.html#inflex.verb.Verb.is_past_part>`_: Return whether this verb is in past participle form.

        >>> verb.is_past_part()
        False

    * `as_regex </api/inflex.verb.html#inflex.verb.Verb.as_regex>`_: Return a re.Pattern which matches any inflected form of the word.

        >>> verb.as_regex()
        re.compile('flying|fly|flown|flies|flew', re.IGNORECASE)

:`Adjective`_: 

    Let's introduce a running example:

        >>> adj = Adjective("pretty")

    * `singular </api/inflex.adjective.html#inflex.adjective.Adjective.singular>`_: Return the singular form of this adjective.

        >>> adj.singular()
        "pretty"

    * `plural </api/inflex.adjective.html#inflex.adjective.Adjective.plural>`_: Return the plural form of this adjective.

        >>> adj.plural()
        "pretty"

    * `comparative </api/inflex.adjective.html#inflex.adjective.Adjective.comparative>`_: Return the comparative form of this adjective.

        >>> adj.singular()
        "prettier"

    * `superlative </api/inflex.adjective.html#inflex.adjective.Adjective.superlative>`_: Return the superlative form of this adjective.

        >>> adj.singular()
        "prettiest"

    * `is_singular </api/inflex.adjective.html#inflex.adjective.Adjective.is_singular>`_: Return whether this adjective is in singular form.

        >>> adj.is_singular()
        True

    * `is_plural </api/inflex.adjective.html#inflex.adjective.Adjective.is_plural>`_:  Return whether this adjective is in plural form.

        >>> adj.is_singular()
        True

    * `as_regex </api/inflex.adjective.html#inflex.adjective.Adjective.as_regex>`_: Return a re.Pattern which matches any inflected form of the word.

        >>> adj.as_regex()
        re.compile('pretty|prettiest|prettier', re.IGNORECASE)

This quick reference is not exhaustive, but does cover the most important functionality supported by Inflex. Feel free to look at the full `API Reference`_ for more detailed information.

.. _Noun: /api/inflex.noun.html#inflex.noun.Noun
.. _Verb: /api/inflex.verb.html#inflex.verb.Verb
.. _Adjective: /api/inflex.adjective.html#inflex.adjective.Adjective
.. _API Reference: /api/inflex.html
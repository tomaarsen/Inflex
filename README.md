# Inflex
Natural Language Inflection in English<br>
(Formerly called Inflexion)

---

This README is a stub, and is yet to be written.

---

## Install
Inflex has no module requirements, and has support for Python version 3.7 onwards.<br>
Install it via:
```
pip install inflex
```

## Sample Usage
```python
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
```

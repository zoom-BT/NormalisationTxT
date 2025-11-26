"""
Grammaires FST pour la normalisation de texte

Ce package contient les grammaires de transducteurs à états finis (FST)
pour la normalisation des nombres cardinaux en français et en anglais.

Modules:
    - french_cardinals: Grammaire pour les nombres cardinaux français (0-1000)
    - english_cardinals: Grammaire pour les nombres cardinaux anglais (0-1000)

Author: Text Normalization Challenge
Date: 2025
"""

from grammars.french_cardinals import FrenchCardinalFST, create_french_cardinal_fst
from grammars.english_cardinals import EnglishCardinalFST, create_english_cardinal_fst

__all__ = [
    'FrenchCardinalFST',
    'EnglishCardinalFST',
    'create_french_cardinal_fst',
    'create_english_cardinal_fst',
]

__version__ = '1.0.0'

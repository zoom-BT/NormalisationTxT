"""
Module principal de normalisation de texte

Ce package fournit les outils pour normaliser les nombres cardinaux
dans un texte en français ou en anglais en utilisant des FST.

Classes principales:
    - TextNormalizer: Normaliseur de texte principal
    - SentenceNormalizer: Normaliseur pour phrases complètes

Fonctions utilitaires:
    - normalize_text: Fonction simple pour normaliser un texte

Author: Text Normalization Challenge
Date: 2025
"""

from src.text_normalizer import (
    TextNormalizer,
    SentenceNormalizer,
    normalize_text
)

__all__ = [
    'TextNormalizer',
    'SentenceNormalizer',
    'normalize_text',
]

__version__ = '1.0.0'

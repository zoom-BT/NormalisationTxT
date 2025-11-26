"""
Grammaire FST pour les nombres cardinaux français (0-1000)

Cette grammaire convertit les chiffres en leur forme écrite en français.
Exemples:
    - "0" -> "zéro"
    - "21" -> "vingt-et-un"
    - "80" -> "quatre-vingts"
    - "1000" -> "mille"

Author: Text Normalization Challenge
Date: 2025
"""

import pynini
from pynini.lib import rewrite


class FrenchCardinalFST:
    """Constructeur de grammaire FST pour les nombres cardinaux français."""

    def __init__(self):
        """Initialize the French cardinal number FST."""
        self.fst = self._build_fst()

    def _build_fst(self) -> pynini.Fst:
        """
        Construit le transducteur à états finis pour les nombres cardinaux français.

        Returns:
            pynini.Fst: Le FST compilé pour la normalisation des nombres
        """
        # Chiffres de base (0-16)
        digits_0_16 = pynini.string_map([
            ("0", "zéro"),
            ("1", "un"),
            ("2", "deux"),
            ("3", "trois"),
            ("4", "quatre"),
            ("5", "cinq"),
            ("6", "six"),
            ("7", "sept"),
            ("8", "huit"),
            ("9", "neuf"),
            ("10", "dix"),
            ("11", "onze"),
            ("12", "douze"),
            ("13", "treize"),
            ("14", "quatorze"),
            ("15", "quinze"),
            ("16", "seize"),
        ])

        # 17-19
        digits_17_19 = pynini.string_map([
            ("17", "dix-sept"),
            ("18", "dix-huit"),
            ("19", "dix-neuf"),
        ])

        # Dizaines (20, 30, 40, 50, 60)
        tens_map = pynini.string_map([
            ("20", "vingt"),
            ("30", "trente"),
            ("40", "quarante"),
            ("50", "cinquante"),
            ("60", "soixante"),
        ])

        # Unités pour composition (1-9)
        units_for_composition = pynini.string_map([
            ("1", "un"),
            ("2", "deux"),
            ("3", "trois"),
            ("4", "quatre"),
            ("5", "cinq"),
            ("6", "six"),
            ("7", "sept"),
            ("8", "huit"),
            ("9", "neuf"),
        ])

        # 21-69 (sauf 20, 30, 40, 50, 60)
        # Construction: dizaine + "-" + unité, sauf pour 21, 31, 41, 51, 61 qui utilisent "et"
        twenty_to_sixty_nine = pynini.Fst()

        # Pour 21, 31, 41, 51, 61 (avec "et")
        et_numbers = pynini.string_map([
            ("21", "vingt-et-un"),
            ("31", "trente-et-un"),
            ("41", "quarante-et-un"),
            ("51", "cinquante-et-un"),
            ("61", "soixante-et-un"),
        ])

        # Pour les autres (22-29, 32-39, 42-49, 52-59, 62-69)
        hyphen_numbers = pynini.Fst()
        for ten, ten_word in [("2", "vingt"), ("3", "trente"), ("4", "quarante"),
                               ("5", "cinquante"), ("6", "soixante")]:
            for unit in ["2", "3", "4", "5", "6", "7", "8", "9"]:
                number = ten + unit
                unit_word = {
                    "2": "deux", "3": "trois", "4": "quatre", "5": "cinq",
                    "6": "six", "7": "sept", "8": "huit", "9": "neuf"
                }[unit]
                hyphen_numbers |= pynini.cross(number, f"{ten_word}-{unit_word}")

        # 70-79 (soixante-dix, soixante et onze, soixante-douze, etc.)
        seventy_map = pynini.string_map([
            ("70", "soixante-dix"),
            ("71", "soixante et onze"),
            ("72", "soixante-douze"),
            ("73", "soixante-treize"),
            ("74", "soixante-quatorze"),
            ("75", "soixante-quinze"),
            ("76", "soixante-seize"),
            ("77", "soixante-dix-sept"),
            ("78", "soixante-dix-huit"),
            ("79", "soixante-dix-neuf"),
        ])

        # 80-99 (quatre-vingts, quatre-vingt-un, etc.)
        eighty_map = pynini.string_map([
            ("80", "quatre-vingts"),
            ("81", "quatre-vingt-un"),
            ("82", "quatre-vingt-deux"),
            ("83", "quatre-vingt-trois"),
            ("84", "quatre-vingt-quatre"),
            ("85", "quatre-vingt-cinq"),
            ("86", "quatre-vingt-six"),
            ("87", "quatre-vingt-sept"),
            ("88", "quatre-vingt-huit"),
            ("89", "quatre-vingt-neuf"),
            ("90", "quatre-vingt-dix"),
            ("91", "quatre-vingt-onze"),
            ("92", "quatre-vingt-douze"),
            ("93", "quatre-vingt-treize"),
            ("94", "quatre-vingt-quatorze"),
            ("95", "quatre-vingt-quinze"),
            ("96", "quatre-vingt-seize"),
            ("97", "quatre-vingt-dix-sept"),
            ("98", "quatre-vingt-dix-huit"),
            ("99", "quatre-vingt-dix-neuf"),
        ])

        # Union de tous les nombres 0-99
        zero_to_ninetynine = (
            digits_0_16 | digits_17_19 | tens_map |
            et_numbers | hyphen_numbers | seventy_map | eighty_map
        )

        # Centaines (100-999)
        hundreds = pynini.Fst()

        # 100
        hundreds |= pynini.cross("100", "cent")

        # 200-900 (avec "s" pour les centaines exactes)
        for h in range(2, 10):
            h_word = {
                2: "deux", 3: "trois", 4: "quatre", 5: "cinq",
                6: "six", 7: "sept", 8: "huit", 9: "neuf"
            }[h]
            # Centaine exacte (avec "s")
            hundreds |= pynini.cross(f"{h}00", f"{h_word}-cents")

        # 101-999 (avec dizaines et unités)
        for h in range(1, 10):
            if h == 1:
                h_prefix = "cent"
            else:
                h_word = {
                    2: "deux", 3: "trois", 4: "quatre", 5: "cinq",
                    6: "six", 7: "sept", 8: "huit", 9: "neuf"
                }[h]
                h_prefix = f"{h_word}-cent"

            # Composition avec les nombres 1-99
            for i in range(1, 100):
                number = f"{h}{i:02d}"
                # Utiliser le FST zero_to_ninetynine pour obtenir la forme écrite
                tens_units = str(i)

                # Mapping manuel pour éviter la complexité de réutilisation
                tens_units_words = self._get_tens_units_word(i)
                hundreds |= pynini.cross(number, f"{h_prefix}-{tens_units_words}")

        # 1000
        thousand = pynini.cross("1000", "mille")

        # Union finale
        final_fst = zero_to_ninetynine | hundreds | thousand

        return final_fst.optimize()

    def _get_tens_units_word(self, number: int) -> str:
        """
        Convertit un nombre de 1-99 en sa forme écrite française.

        Args:
            number: Nombre entre 1 et 99

        Returns:
            str: Forme écrite du nombre
        """
        mapping = {
            1: "un", 2: "deux", 3: "trois", 4: "quatre", 5: "cinq",
            6: "six", 7: "sept", 8: "huit", 9: "neuf", 10: "dix",
            11: "onze", 12: "douze", 13: "treize", 14: "quatorze", 15: "quinze", 16: "seize",
            17: "dix-sept", 18: "dix-huit", 19: "dix-neuf",
            20: "vingt", 21: "vingt-et-un", 22: "vingt-deux", 23: "vingt-trois", 24: "vingt-quatre",
            25: "vingt-cinq", 26: "vingt-six", 27: "vingt-sept", 28: "vingt-huit", 29: "vingt-neuf",
            30: "trente", 31: "trente-et-un", 32: "trente-deux", 33: "trente-trois", 34: "trente-quatre",
            35: "trente-cinq", 36: "trente-six", 37: "trente-sept", 38: "trente-huit", 39: "trente-neuf",
            40: "quarante", 41: "quarante-et-un", 42: "quarante-deux", 43: "quarante-trois", 44: "quarante-quatre",
            45: "quarante-cinq", 46: "quarante-six", 47: "quarante-sept", 48: "quarante-huit", 49: "quarante-neuf",
            50: "cinquante", 51: "cinquante-et-un", 52: "cinquante-deux", 53: "cinquante-trois", 54: "cinquante-quatre",
            55: "cinquante-cinq", 56: "cinquante-six", 57: "cinquante-sept", 58: "cinquante-huit", 59: "cinquante-neuf",
            60: "soixante", 61: "soixante-et-un", 62: "soixante-deux", 63: "soixante-trois", 64: "soixante-quatre",
            65: "soixante-cinq", 66: "soixante-six", 67: "soixante-sept", 68: "soixante-huit", 69: "soixante-neuf",
            70: "soixante-dix", 71: "soixante et onze", 72: "soixante-douze", 73: "soixante-treize", 74: "soixante-quatorze",
            75: "soixante-quinze", 76: "soixante-seize", 77: "soixante-dix-sept", 78: "soixante-dix-huit", 79: "soixante-dix-neuf",
            80: "quatre-vingts", 81: "quatre-vingt-un", 82: "quatre-vingt-deux", 83: "quatre-vingt-trois", 84: "quatre-vingt-quatre",
            85: "quatre-vingt-cinq", 86: "quatre-vingt-six", 87: "quatre-vingt-sept", 88: "quatre-vingt-huit", 89: "quatre-vingt-neuf",
            90: "quatre-vingt-dix", 91: "quatre-vingt-onze", 92: "quatre-vingt-douze", 93: "quatre-vingt-treize", 94: "quatre-vingt-quatorze",
            95: "quatre-vingt-quinze", 96: "quatre-vingt-seize", 97: "quatre-vingt-dix-sept", 98: "quatre-vingt-dix-huit", 99: "quatre-vingt-dix-neuf",
        }
        return mapping[number]

    def normalize(self, text: str) -> str:
        """
        Normalise un nombre en sa forme écrite.

        Args:
            text: Nombre sous forme de chaîne (ex: "42")

        Returns:
            str: Forme écrite du nombre (ex: "quarante-deux")
        """
        try:
            result = rewrite.one_top_rewrite(text, self.fst)
            return result
        except Exception as e:
            # Si la normalisation échoue, retourner le texte original
            return text

    def get_fst(self) -> pynini.Fst:
        """Retourne le FST compilé."""
        return self.fst


def create_french_cardinal_fst() -> pynini.Fst:
    """
    Fonction utilitaire pour créer le FST des nombres cardinaux français.

    Returns:
        pynini.Fst: FST compilé pour les nombres cardinaux français
    """
    builder = FrenchCardinalFST()
    return builder.get_fst()


if __name__ == "__main__":
    # Tests rapides
    fst_builder = FrenchCardinalFST()

    test_cases = [
        "0", "1", "7", "10", "15", "17", "21", "42", "70", "71", "80", "99", "100", "200", "999", "1000"
    ]

    print("Tests de normalisation française:")
    print("-" * 50)
    for num in test_cases:
        normalized = fst_builder.normalize(num)
        print(f"{num:>4} -> {normalized}")

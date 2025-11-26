"""
Grammaire FST pour les nombres cardinaux anglais (0-1000)

Cette grammaire convertit les chiffres en leur forme écrite en anglais.
Exemples:
    - "0" -> "zero"
    - "21" -> "twenty-one"
    - "100" -> "one hundred"
    - "1000" -> "one thousand"

Author: Text Normalization Challenge
Date: 2025
"""

import pynini
from pynini.lib import rewrite


class EnglishCardinalFST:
    """Constructeur de grammaire FST pour les nombres cardinaux anglais."""

    def __init__(self):
        """Initialize the English cardinal number FST."""
        self.fst = self._build_fst()

    def _build_fst(self) -> pynini.Fst:
        """
        Construit le transducteur à états finis pour les nombres cardinaux anglais.

        Returns:
            pynini.Fst: Le FST compilé pour la normalisation des nombres
        """
        # Chiffres de base (0-19)
        digits_0_19 = pynini.string_map([
            ("0", "zero"),
            ("1", "one"),
            ("2", "two"),
            ("3", "three"),
            ("4", "four"),
            ("5", "five"),
            ("6", "six"),
            ("7", "seven"),
            ("8", "eight"),
            ("9", "nine"),
            ("10", "ten"),
            ("11", "eleven"),
            ("12", "twelve"),
            ("13", "thirteen"),
            ("14", "fourteen"),
            ("15", "fifteen"),
            ("16", "sixteen"),
            ("17", "seventeen"),
            ("18", "eighteen"),
            ("19", "nineteen"),
        ])

        # Dizaines (20, 30, 40, ..., 90)
        tens_map = pynini.string_map([
            ("20", "twenty"),
            ("30", "thirty"),
            ("40", "forty"),
            ("50", "fifty"),
            ("60", "sixty"),
            ("70", "seventy"),
            ("80", "eighty"),
            ("90", "ninety"),
        ])

        # Nombres composés 21-99 (sauf dizaines exactes)
        twenty_to_ninetynine = pynini.Fst()
        tens_words = {
            "2": "twenty", "3": "thirty", "4": "forty", "5": "fifty",
            "6": "sixty", "7": "seventy", "8": "eighty", "9": "ninety"
        }
        units_words = {
            "1": "one", "2": "two", "3": "three", "4": "four", "5": "five",
            "6": "six", "7": "seven", "8": "eight", "9": "nine"
        }

        for ten_digit, ten_word in tens_words.items():
            for unit_digit, unit_word in units_words.items():
                number = ten_digit + unit_digit
                twenty_to_ninetynine |= pynini.cross(number, f"{ten_word}-{unit_word}")

        # Union de tous les nombres 0-99
        zero_to_ninetynine = digits_0_19 | tens_map | twenty_to_ninetynine

        # Centaines (100-999)
        hundreds = pynini.Fst()

        # Centaines exactes (100, 200, ..., 900)
        for h in range(1, 10):
            h_word = {
                1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
                6: "six", 7: "seven", 8: "eight", 9: "nine"
            }[h]
            hundreds |= pynini.cross(f"{h}00", f"{h_word} hundred")

        # Centaines avec dizaines et unités (101-999)
        for h in range(1, 10):
            h_word = {
                1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
                6: "six", 7: "seven", 8: "eight", 9: "nine"
            }[h]

            for i in range(1, 100):
                number = f"{h}{i:02d}"
                tens_units_word = self._get_tens_units_word(i)
                hundreds |= pynini.cross(number, f"{h_word} hundred {tens_units_word}")

        # 1000
        thousand = pynini.cross("1000", "one thousand")

        # Union finale
        final_fst = zero_to_ninetynine | hundreds | thousand

        return final_fst.optimize()

    def _get_tens_units_word(self, number: int) -> str:
        """
        Convertit un nombre de 1-99 en sa forme écrite anglaise.

        Args:
            number: Nombre entre 1 et 99

        Returns:
            str: Forme écrite du nombre
        """
        mapping = {
            1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
            6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
            11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
            15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen",
            20: "twenty", 21: "twenty-one", 22: "twenty-two", 23: "twenty-three",
            24: "twenty-four", 25: "twenty-five", 26: "twenty-six", 27: "twenty-seven",
            28: "twenty-eight", 29: "twenty-nine",
            30: "thirty", 31: "thirty-one", 32: "thirty-two", 33: "thirty-three",
            34: "thirty-four", 35: "thirty-five", 36: "thirty-six", 37: "thirty-seven",
            38: "thirty-eight", 39: "thirty-nine",
            40: "forty", 41: "forty-one", 42: "forty-two", 43: "forty-three",
            44: "forty-four", 45: "forty-five", 46: "forty-six", 47: "forty-seven",
            48: "forty-eight", 49: "forty-nine",
            50: "fifty", 51: "fifty-one", 52: "fifty-two", 53: "fifty-three",
            54: "fifty-four", 55: "fifty-five", 56: "fifty-six", 57: "fifty-seven",
            58: "fifty-eight", 59: "fifty-nine",
            60: "sixty", 61: "sixty-one", 62: "sixty-two", 63: "sixty-three",
            64: "sixty-four", 65: "sixty-five", 66: "sixty-six", 67: "sixty-seven",
            68: "sixty-eight", 69: "sixty-nine",
            70: "seventy", 71: "seventy-one", 72: "seventy-two", 73: "seventy-three",
            74: "seventy-four", 75: "seventy-five", 76: "seventy-six", 77: "seventy-seven",
            78: "seventy-eight", 79: "seventy-nine",
            80: "eighty", 81: "eighty-one", 82: "eighty-two", 83: "eighty-three",
            84: "eighty-four", 85: "eighty-five", 86: "eighty-six", 87: "eighty-seven",
            88: "eighty-eight", 89: "eighty-nine",
            90: "ninety", 91: "ninety-one", 92: "ninety-two", 93: "ninety-three",
            94: "ninety-four", 95: "ninety-five", 96: "ninety-six", 97: "ninety-seven",
            98: "ninety-eight", 99: "ninety-nine",
        }
        return mapping[number]

    def normalize(self, text: str) -> str:
        """
        Normalise un nombre en sa forme écrite.

        Args:
            text: Nombre sous forme de chaîne (ex: "42")

        Returns:
            str: Forme écrite du nombre (ex: "forty-two")
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


def create_english_cardinal_fst() -> pynini.Fst:
    """
    Fonction utilitaire pour créer le FST des nombres cardinaux anglais.

    Returns:
        pynini.Fst: FST compilé pour les nombres cardinaux anglais
    """
    builder = EnglishCardinalFST()
    return builder.get_fst()


if __name__ == "__main__":
    # Tests rapides
    fst_builder = EnglishCardinalFST()

    test_cases = [
        "0", "1", "7", "10", "15", "21", "42", "70", "99", "100", "200", "999", "1000"
    ]

    print("Tests de normalisation anglaise:")
    print("-" * 50)
    for num in test_cases:
        normalized = fst_builder.normalize(num)
        print(f"{num:>4} -> {normalized}")

#!/usr/bin/env python3
"""
Script de vérification de la soumission

Ce script vérifie que tous les fichiers requis sont présents
et que la structure du projet est correcte.

Author: Text Normalization Challenge
Date: 2025
"""

import os
import sys
from pathlib import Path


class SubmissionChecker:
    """Vérificateur de soumission."""

    def __init__(self):
        """Initialise le vérificateur."""
        self.root = Path(__file__).parent
        self.errors = []
        self.warnings = []
        self.checks_passed = 0
        self.checks_total = 0

    def check_file(self, path: str, description: str, required: bool = True) -> bool:
        """
        Vérifie qu'un fichier existe.

        Args:
            path: Chemin relatif du fichier
            description: Description du fichier
            required: Si True, l'absence est une erreur, sinon un warning

        Returns:
            bool: True si le fichier existe
        """
        self.checks_total += 1
        full_path = self.root / path

        if full_path.exists():
            print(f"✓ {description}")
            self.checks_passed += 1
            return True
        else:
            if required:
                self.errors.append(f"Fichier manquant: {path} ({description})")
                print(f"✗ {description} - MANQUANT")
            else:
                self.warnings.append(f"Fichier optionnel absent: {path}")
                print(f"⚠ {description} - optionnel, non trouvé")
            return False

    def check_directory(self, path: str, description: str) -> bool:
        """Vérifie qu'un répertoire existe."""
        self.checks_total += 1
        full_path = self.root / path

        if full_path.exists() and full_path.is_dir():
            print(f"✓ {description}")
            self.checks_passed += 1
            return True
        else:
            self.errors.append(f"Répertoire manquant: {path}")
            print(f"✗ {description} - MANQUANT")
            return False

    def run_all_checks(self):
        """Exécute toutes les vérifications."""
        print("=" * 70)
        print("VÉRIFICATION DE LA SOUMISSION")
        print("=" * 70)
        print()

        # 1. Structure des répertoires
        print("1. Structure des répertoires:")
        print("-" * 70)
        self.check_directory("grammars", "Répertoire des grammaires")
        self.check_directory("src", "Répertoire du code source")
        self.check_directory("tests", "Répertoire des tests")
        self.check_directory("docs", "Répertoire de la documentation")
        self.check_directory("examples", "Répertoire des exemples")
        print()

        # 2. Code source Python
        print("2. Code source Python:")
        print("-" * 70)
        self.check_file("grammars/french_cardinals.py", "Grammaire française")
        self.check_file("grammars/english_cardinals.py", "Grammaire anglaise")
        self.check_file("grammars/__init__.py", "Init grammars")
        self.check_file("src/text_normalizer.py", "Module de normalisation")
        self.check_file("src/compile_fst.py", "Script de compilation FST")
        self.check_file("src/__init__.py", "Init src")
        self.check_file("normalize.py", "Script CLI principal")
        print()

        # 3. Tests
        print("3. Tests unitaires:")
        print("-" * 70)
        self.check_file("tests/test_cardinals.py", "Tests des cardinaux")
        self.check_file("tests/__init__.py", "Init tests")
        print()

        # 4. Documentation
        print("4. Documentation:")
        print("-" * 70)
        self.check_file("README.md", "README principal")
        self.check_file("requirements.txt", "Liste des dépendances")
        self.check_file("INSTALLATION.md", "Guide d'installation")
        self.check_file("SUBMISSION.md", "Guide de soumission")
        self.check_file("docs/generate_report.py", "Générateur de rapport PDF")
        print()

        # 5. Exemples
        print("5. Exemples:")
        print("-" * 70)
        self.check_file("examples/demo.py", "Démonstration complète")
        self.check_file("examples/quick_demo.py", "Démonstration rapide")
        self.check_file("examples/example_input.txt", "Fichier exemple")
        print()

        # 6. Fichiers compilés (optionnels)
        print("6. Fichiers compilés (générés après compilation):")
        print("-" * 70)
        self.check_file("compiled/french_cardinals.fst", "FST français compilé", required=False)
        self.check_file("compiled/english_cardinals.fst", "FST anglais compilé", required=False)
        self.check_file("docs/report.pdf", "Rapport PDF", required=False)
        print()

        # Résumé
        self.print_summary()

    def print_summary(self):
        """Affiche le résumé des vérifications."""
        print("=" * 70)
        print("RÉSUMÉ")
        print("=" * 70)
        print()

        success_rate = (self.checks_passed / self.checks_total * 100) if self.checks_total > 0 else 0

        print(f"Vérifications réussies: {self.checks_passed}/{self.checks_total} ({success_rate:.1f}%)")
        print()

        if self.errors:
            print("ERREURS:")
            for error in self.errors:
                print(f"  ✗ {error}")
            print()

        if self.warnings:
            print("AVERTISSEMENTS:")
            for warning in self.warnings:
                print(f"  ⚠ {warning}")
            print()

        if not self.errors:
            print("✓ Tous les fichiers requis sont présents!")
            print()
            print("PROCHAINES ÉTAPES:")
            print("  1. Installer les dépendances: pip install -r requirements.txt")
            print("  2. Compiler les FST: python src/compile_fst.py")
            print("  3. Générer le rapport: python docs/generate_report.py")
            print("  4. Tester le système: python normalize.py --demo")
            print("  5. Lancer les tests: pytest tests/ -v")
            print()
            print("La soumission est prête! 🎉")
        else:
            print("✗ Certains fichiers requis sont manquants.")
            print("Veuillez corriger les erreurs avant de soumettre.")
            sys.exit(1)


def main():
    """Point d'entrée principal."""
    checker = SubmissionChecker()
    checker.run_all_checks()


if __name__ == "__main__":
    main()

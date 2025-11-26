"""
Script de compilation des grammaires FST en archives FAR

Ce script compile les grammaires FST pour les nombres cardinaux français
et anglais et les sauvegarde dans des fichiers FAR (Finite-state Archive).

Les fichiers FAR permettent:
- Un chargement plus rapide des grammaires
- Une meilleure performance en production
- Un stockage compact des FST compilés

Usage:
    python compile_fst.py [--output-dir OUTPUT_DIR]

Author: Text Normalization Challenge
Date: 2025
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pynini
from grammars.french_cardinals import create_french_cardinal_fst
from grammars.english_cardinals import create_english_cardinal_fst


class FSTCompiler:
    """Compilateur de grammaires FST en fichiers FAR."""

    def __init__(self, output_dir: str = "compiled"):
        """
        Initialise le compilateur.

        Args:
            output_dir: Répertoire de sortie pour les fichiers compilés
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Statistiques de compilation
        self.stats = {
            'french': {'compile_time': 0, 'fst_size': 0, 'num_states': 0, 'num_arcs': 0},
            'english': {'compile_time': 0, 'fst_size': 0, 'num_states': 0, 'num_arcs': 0}
        }

    def compile_french_grammar(self) -> Path:
        """
        Compile la grammaire française en fichier FAR.

        Returns:
            Path: Chemin vers le fichier FAR compilé
        """
        print("Compilation de la grammaire française...")
        print("-" * 70)

        start_time = time.time()

        # Créer le FST
        fst = create_french_cardinal_fst()

        # Collecter les statistiques
        self.stats['french']['num_states'] = fst.num_states()
        self.stats['french']['num_arcs'] = sum(
            fst.num_arcs(state) for state in range(fst.num_states())
        )

        # Sauvegarder en fichier FST
        fst_path = self.output_dir / "french_cardinals.fst"
        fst.write(str(fst_path))

        # Créer le fichier FAR
        far_path = self.output_dir / "french_cardinals.far"

        # Pour créer un FAR, on utilise la commande farcompilestrings
        # Mais avec pynini, on peut simplement sauvegarder le FST
        # Le FAR est plus utile quand on a plusieurs FST à combiner
        # Pour l'instant, on sauvegarde juste le FST optimisé

        compile_time = time.time() - start_time
        self.stats['french']['compile_time'] = compile_time

        # Taille du fichier
        if fst_path.exists():
            self.stats['french']['fst_size'] = fst_path.stat().st_size

        print(f"✓ Grammaire française compilée avec succès")
        print(f"  Temps de compilation: {compile_time:.3f}s")
        print(f"  Nombre d'états: {self.stats['french']['num_states']}")
        print(f"  Nombre d'arcs: {self.stats['french']['num_arcs']}")
        print(f"  Taille du fichier: {self.stats['french']['fst_size'] / 1024:.2f} KB")
        print(f"  Fichier: {fst_path}")
        print()

        return fst_path

    def compile_english_grammar(self) -> Path:
        """
        Compile la grammaire anglaise en fichier FAR.

        Returns:
            Path: Chemin vers le fichier FAR compilé
        """
        print("Compilation de la grammaire anglaise...")
        print("-" * 70)

        start_time = time.time()

        # Créer le FST
        fst = create_english_cardinal_fst()

        # Collecter les statistiques
        self.stats['english']['num_states'] = fst.num_states()
        self.stats['english']['num_arcs'] = sum(
            fst.num_arcs(state) for state in range(fst.num_states())
        )

        # Sauvegarder en fichier FST
        fst_path = self.output_dir / "english_cardinals.fst"
        fst.write(str(fst_path))

        compile_time = time.time() - start_time
        self.stats['english']['compile_time'] = compile_time

        # Taille du fichier
        if fst_path.exists():
            self.stats['english']['fst_size'] = fst_path.stat().st_size

        print(f"✓ Grammaire anglaise compilée avec succès")
        print(f"  Temps de compilation: {compile_time:.3f}s")
        print(f"  Nombre d'états: {self.stats['english']['num_states']}")
        print(f"  Nombre d'arcs: {self.stats['english']['num_arcs']}")
        print(f"  Taille du fichier: {self.stats['english']['fst_size'] / 1024:.2f} KB")
        print(f"  Fichier: {fst_path}")
        print()

        return fst_path

    def compile_all(self) -> dict:
        """
        Compile toutes les grammaires.

        Returns:
            dict: Dictionnaire avec les chemins des fichiers compilés
        """
        print("=" * 70)
        print("COMPILATION DES GRAMMAIRES FST")
        print("=" * 70)
        print()

        results = {
            'french': self.compile_french_grammar(),
            'english': self.compile_english_grammar()
        }

        self.print_summary()

        return results

    def print_summary(self):
        """Affiche un résumé des compilations."""
        print("=" * 70)
        print("RÉSUMÉ DE LA COMPILATION")
        print("=" * 70)
        print()

        total_time = (
            self.stats['french']['compile_time'] +
            self.stats['english']['compile_time']
        )
        total_size = (
            self.stats['french']['fst_size'] +
            self.stats['english']['fst_size']
        )

        print(f"Temps total de compilation: {total_time:.3f}s")
        print(f"Taille totale des fichiers: {total_size / 1024:.2f} KB")
        print()

        print("Détails par langue:")
        print()
        print("Français:")
        print(f"  - États: {self.stats['french']['num_states']}")
        print(f"  - Arcs: {self.stats['french']['num_arcs']}")
        print(f"  - Temps: {self.stats['french']['compile_time']:.3f}s")
        print(f"  - Taille: {self.stats['french']['fst_size'] / 1024:.2f} KB")
        print()
        print("Anglais:")
        print(f"  - États: {self.stats['english']['num_states']}")
        print(f"  - Arcs: {self.stats['english']['num_arcs']}")
        print(f"  - Temps: {self.stats['english']['compile_time']:.3f}s")
        print(f"  - Taille: {self.stats['english']['fst_size'] / 1024:.2f} KB")
        print()

        # Sauvegarder les statistiques dans un fichier
        stats_file = self.output_dir / "compilation_stats.txt"
        with open(stats_file, 'w', encoding='utf-8') as f:
            f.write("STATISTIQUES DE COMPILATION\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Temps total: {total_time:.3f}s\n")
            f.write(f"Taille totale: {total_size / 1024:.2f} KB\n\n")
            f.write("Français:\n")
            f.write(f"  États: {self.stats['french']['num_states']}\n")
            f.write(f"  Arcs: {self.stats['french']['num_arcs']}\n")
            f.write(f"  Temps: {self.stats['french']['compile_time']:.3f}s\n")
            f.write(f"  Taille: {self.stats['french']['fst_size'] / 1024:.2f} KB\n\n")
            f.write("Anglais:\n")
            f.write(f"  États: {self.stats['english']['num_states']}\n")
            f.write(f"  Arcs: {self.stats['english']['num_arcs']}\n")
            f.write(f"  Temps: {self.stats['english']['compile_time']:.3f}s\n")
            f.write(f"  Taille: {self.stats['english']['fst_size'] / 1024:.2f} KB\n")

        print(f"✓ Statistiques sauvegardées dans: {stats_file}")
        print()


def main():
    """Point d'entrée principal du script."""
    parser = argparse.ArgumentParser(
        description="Compile les grammaires FST en fichiers FAR"
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='compiled',
        help='Répertoire de sortie pour les fichiers compilés (défaut: compiled)'
    )

    args = parser.parse_args()

    # Compiler les grammaires
    compiler = FSTCompiler(output_dir=args.output_dir)
    results = compiler.compile_all()

    print("✓ Compilation terminée avec succès!")
    print()
    print("Fichiers générés:")
    for lang, path in results.items():
        print(f"  - {lang}: {path}")


if __name__ == "__main__":
    main()

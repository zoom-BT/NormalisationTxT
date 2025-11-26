# Guide d'installation détaillé

## Prérequis

- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)
- Système d'exploitation: Linux, macOS, ou Windows avec WSL

## Installation de Pynini

Pynini nécessite OpenFST. Voici les instructions d'installation par système:

### Linux (Ubuntu/Debian)

```bash
# Installer les dépendances système
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    python3-dev \
    wget \
    autoconf \
    libtool

# Option 1: Installation via pip (recommandé)
pip install pynini

# Option 2: Installation depuis les sources
# Si l'option 1 ne fonctionne pas, consulter:
# https://www.openfst.org/twiki/bin/view/FST/PyniniDownload
```

### macOS

```bash
# Installer Homebrew si nécessaire
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installer les dépendances
brew install openfst

# Installer pynini
pip install pynini
```

### Windows

Utiliser WSL (Windows Subsystem for Linux) et suivre les instructions Linux.

```bash
# Dans WSL Ubuntu
wsl --install
# Puis suivre les instructions Linux ci-dessus
```

## Installation du projet

### 1. Cloner le dépôt

```bash
git clone <url-du-depot>
cd NormalisationTxT
```

### 2. Créer un environnement virtuel (recommandé)

```bash
# Créer l'environnement
python3 -m venv venv

# Activer l'environnement
# Linux/macOS:
source venv/bin/activate

# Windows (WSL):
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Vérifier l'installation

```bash
# Test rapide
python -c "import pynini; print('Pynini installé avec succès!')"

# Exécuter la démo
python normalize.py --demo
```

### 5. Compiler les grammaires FST

```bash
python src/compile_fst.py --output-dir compiled
```

## Résolution de problèmes

### Erreur: "pynini not found"

Si `pip install pynini` échoue:

1. Vérifiez que vous avez Python 3.7+:
   ```bash
   python --version
   ```

2. Installez les outils de compilation:
   ```bash
   sudo apt-get install build-essential python3-dev
   ```

3. Essayez d'installer une version spécifique:
   ```bash
   pip install pynini==2.1.5
   ```

### Erreur: "OpenFST not found"

OpenFST doit être installé avant Pynini:

```bash
# Linux
sudo apt-get install libfst-dev

# macOS
brew install openfst
```

### Tests sans Pynini (mode dégradé)

Si vous ne pouvez pas installer Pynini, vous pouvez consulter le code et la documentation:

```bash
# Voir le code des grammaires
cat grammars/french_cardinals.py
cat grammars/english_cardinals.py

# Lire le rapport
# Ouvrir docs/report.pdf
```

## Installation minimale (sans Pynini)

Si vous voulez juste consulter le code et la documentation sans exécuter le système:

```bash
# Installer uniquement les dépendances pour la documentation
pip install reportlab matplotlib

# Générer le rapport PDF
python docs/generate_report.py
```

## Validation de l'installation

Après l'installation, exécutez les tests:

```bash
# Tests unitaires
pytest tests/ -v

# Tests manuels
python tests/test_cardinals.py

# Démonstration complète
python examples/demo.py
```

## Support

En cas de problème:

1. Vérifiez les versions:
   ```bash
   python --version
   pip --version
   python -c "import pynini; print(pynini.__version__)"
   ```

2. Consultez la documentation Pynini:
   - https://www.openfst.org/twiki/bin/view/FST/PyniniDownload
   - https://github.com/kylebgorman/pynini

3. Vérifiez les issues GitHub du projet Pynini

## Installation réussie

Si tout fonctionne, vous devriez pouvoir exécuter:

```bash
python normalize.py "J'ai 3 chiens" --lang fr
# Sortie attendue: J'ai trois chiens

python normalize.py "I have 42 cats" --lang en
# Sortie attendue: I have forty-two cats
```

Félicitations! 🎉 Le système est prêt à être utilisé.

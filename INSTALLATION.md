wsl --install
# Guide d'installation

Ce projet utilise `pynini`, une bibliothèque qui dépend de librairies C++ Unix.

⚠️ **ATTENTION UTILISATEURS WINDOWS** ⚠️
Ce projet **NE FONCTIONNE PAS** nativement sur Windows PowerShell ou CMD.
Vous **DEVEZ** utiliser **WSL (Windows Subsystem for Linux)**.

## 🐧 Installation sur Linux / macOS / WSL

### 1. Prérequis système

Assurez-vous d'avoir les outils de compilation installés (nécessaire pour compiler Pynini).

**Ubuntu / Debian / WSL :**
```bash
sudo apt-get update
sudo apt-get install -y build-essential python3-dev
```

# macOS
xcode-select --install

# Installation du projet
# Créer un environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# 1. Installer Cython en premier (indispensable pour la compilation)
pip install Cython

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Vérification
python normalize.py --demo
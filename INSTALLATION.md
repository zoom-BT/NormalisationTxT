wsl --install
# Guide d'installation

Ce projet utilise `pynini`, une bibliothèque qui dépend de librairies C++ Unix.

⚠️ **ATTENTION UTILISATEURS WINDOWS** ⚠️
Ce projet **NE FONCTIONNE PAS** nativement sur Windows PowerShell ou CMD.
Vous **DEVEZ** utiliser **WSL (Windows Subsystem for Linux)**.

---

Si vous n'avez pas encore WSL :

1.  Ouvrez **PowerShell** en tant qu'administrateur (Clic droit > Exécuter en tant qu'administrateur).
2.  Tapez la commande suivante et validez :
    ```powershell
    wsl --install
    ```
3.  Une fois l'installation terminée, **redémarrez votre ordinateur**.
4.  Au redémarrage, une fenêtre s'ouvrira automatiquement pour configurer votre nom d'utilisateur et mot de passe Linux (retenez-les bien !).
    *   *Si la fenêtre ne s'ouvre pas, cherchez "Ubuntu" dans le menu Démarrer.*

Vous êtes maintenant dans un terminal Linux (Ubuntu) sur votre machine Windows. C'est ici que tout se passe.

---


## 🐧 Installation sur Linux / macOS / WSL
Toutes les commandes suivantes doivent être exécutées dans le terminal Linux (ou macOS).

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

*Note : L'installation de Pynini peut prendre quelques minutes car elle compile du code C++ en arrière-plan.*

### 3. Vérification

Pour vérifier que tout est correctement installé et configuré :

# 3. Vérification
python normalize.py --demo


Si vous voyez la liste des phrases normalisées s'afficher, félicitations ! L'installation est réussie.

---

## 🛠️ Dépannage (FAQ)

**Erreur : `ModuleNotFoundError: No module named 'Cython'`**
> **Cause** : Pynini essaie de s'installer avant Cython.
> **Solution** : Lancez manuellement `pip install Cython` avant de lancer `pip install -r requirements.txt`.

**Erreur : `Failed to build pynini` ou `command 'gcc' failed`**
> **Cause** : Il manque les outils de compilation sur votre système.
> **Solution** : Vérifiez que vous avez bien exécuté l'étape 1 (`sudo apt-get install build-essential python3-dev`).

**Erreur : `python: can't open file 'normalize.py'`**
> **Cause** : Vous n'êtes pas dans le bon dossier.
> **Solution** : Utilisez la commande `cd` pour aller dans le dossier du projet (ex: `cd NormalisationTxT`).
# 🧪 IA Dev Productivity Sandbox

Un mini-sandbox interactif pour explorer comment l’IA peut améliorer la productivité des développeurs.

Ce projet permet de tester en conditions réelles plusieurs usages clés de l’IA dans un workflow de développement :
- Analyse automatique de fichiers source
- Suggestions de refactorisation / amélioration
- Génération de plans d’onboarding développeur
- Création de checklists qualité / architecture

Il sert à la fois d’outil d’expérimentation, de démonstration pédagogique et de base d’exploration pour l’adoption de l’IA dans les équipes techniques.

---

## 🚀 Fonctionnalités

### 📄 1. Analyse de fichier de code
- Upload d’un fichier (Python, JS, TS, Java, C#…)
- Ou collage direct du code
- L’IA produit :
  - un résumé clair,
  - les risques et points d’attention,
  - des pistes d’amélioration concrètes.

### 🚀 2. Onboarding développeur
L’utilisateur décrit le projet et liste les fichiers importants.
L’IA génère :
- une vue d’ensemble du projet,
- les premières étapes pour prendre en main le code,
- les questions à poser à l’équipe.

### ✅ 3. Checklist qualité / architecture
Modes disponibles :
- Revue générale de code
- Migration monolithe → API-first
- Qualité / dette technique
- Sécurité et authentification

L’IA produit une checklist actionnable et structurée.

---

## 🧩 Architecture

ia-dev-productivity-sandbox/
│
├── app.py # Interface Streamlit + logique métier
├── config.py # Gestion OpenAI (clé, client, modèle)
├── requirements.txt
└── README.md


Responsabilités :
- `app.py` = UI Streamlit + logique métier
- `config.py` = gestion de la clé API + création du client OpenAI

Cette séparation rend l’application plus propre, testable et extensible.

---

## 🐍 Prérequis

### ✔ Python **3.12 obligatoire**

⚠ Streamlit n’est pas compatible avec Python 3.13 au moment de ce projet.

Vérifie ta version :


Téléchargement Python 3.12 :
https://www.python.org/downloads/release/python-3120/

---

## 📦 Installation

### 1. Cloner le repository

git clone https://github.com/Zied-Doura/ia-dev-productivity-sandbox.git
cd ia-dev-productivity-sandbox


### 2. Créer un environnement virtuel

python -m venv .venv


Activer :

**Windows (PowerShell)**  
.venv\Scripts\activate


**macOS / Linux**  
source .venv/bin/activate


### 3. Installer les dépendances

pip install -r requirements.txt


---

# 🔑 Configuration de la clé OpenAI API

Cette application fonctionne avec l’API OpenAI.  
Deux options sont possibles :

---

## 🟢 Option 1 – Variable d’environnement (recommandée)

### Windows (PowerShell)
setx OPENAI_API_KEY "sk-..."


👉 Ferme et rouvre ton terminal

### macOS / Linux
export OPENAI_API_KEY="sk-..."


### Vérifier

**Windows**  
echo $Env:OPENAI_API_KEY


**macOS / Linux**  
echo $OPENAI_API_KEY


---

## 🔵 Option 2 – Entrer la clé dans l’interface Streamlit

Dans la sidebar de l’application :
- Champ "Clé OpenAI API"
- Bouton "Enregistrer la clé API"

La clé reste en session locale et n’est jamais enregistrée.

---

# ▶️ Lancement de l’application
streamlit run app.py


L’application s’ouvre automatiquement dans le navigateur.

---

## 🔍 Exemple d’utilisation

### 1. Analyse de fichier
Charger `order_processor.py` → résumé + risques + améliorations.

### 2. Onboarding
Décrire le projet + fichiers clés → plan d’onboarding structuré.

### 3. Checklist
Choisir "Migration monolithe → API-first" → checklist actionnable.

---

## 🧠 Ce que ce projet démontre

- Exploration concrète de l’IA appliquée au développement
- Structuration d’outils pour équipes techniques
- Architecture propre (séparation config / logique / UI)
- Démarche pédagogique minimisant la barrière d’adoption

Idéal pour :
- la veille technologique,
- les démonstrations internes,
- l’acculturation IA,
- un rôle de Responsable Innovation IA.

---

## 👤 Auteur

Projet personnel développé pour explorer l’adoption de l’IA dans le workflow des développeurs.

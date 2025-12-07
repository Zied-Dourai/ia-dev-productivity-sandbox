# config.py
import os
from typing import Optional

from openai import OpenAI

# Modèle utilisé par défaut
MODEL_NAME = "gpt-4.1-mini"


def get_api_key(explicit_key: Optional[str] = None) -> Optional[str]:
    """
    Récupère la clé API OpenAI.

    Priorité :
    1. explicit_key (par ex. fournie par l'application)
    2. variable d'environnement OPENAI_API_KEY
    """
    if explicit_key:
        return explicit_key

    return os.getenv("OPENAI_API_KEY")


def get_client(explicit_key: Optional[str] = None) -> OpenAI:
    """
    Crée un client OpenAI avec la clé disponible.

    Lève une ValueError si aucune clé n'est trouvée.
    """
    api_key = get_api_key(explicit_key)

    if not api_key:
        raise ValueError(
            "Aucune clé API OpenAI configurée. "
            "Définis OPENAI_API_KEY ou saisis ta clé dans l'interface Streamlit."
        )

    return OpenAI(api_key=api_key)

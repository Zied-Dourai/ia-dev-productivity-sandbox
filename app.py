import os  # si tu ne l'avais plus
import streamlit as st
from datetime import datetime
from typing import List, Dict

from config import get_client, get_api_key, MODEL_NAME

def get_session_api_key() -> str | None:
    """Retourne la clé API éventuellement stockée en session Streamlit."""
    return st.session_state.get("openai_api_key")


MODEL_NAME = "gpt-4.1-mini"


def get_api_key(explicit_key=None):
    """Récupère la clé API dans la session Streamlit ou les variables d'environnement."""
    # Priorité à la clé saisie par l'utilisateur dans l'UI
    key = st.session_state.get("openai_api_key")
    if key:
        return key

    # Sinon, on regarde la variable d'environnement
    return os.getenv("OPENAI_API_KEY")


def call_model(system_prompt: str, user_prompt: str) -> str:
    """Appelle le modèle OpenAI avec une interface simple."""
    try:
        # priorité à la clé saisie dans l'UI (session), sinon env var
        session_key = get_session_api_key()
        client = get_client(explicit_key=session_key)

        response = client.responses.create(
            model=MODEL_NAME,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_output_tokens=800,
        )
        return response.output[0].content[0].text
    except Exception as e:
        return f"Erreur lors de l'appel au modèle : {e}"



def analyze_code(filename: str, code: str) -> Dict[str, str]:
    """Retourne un résumé, des risques, et des suggestions d'amélioration."""
    base_prompt = f"Fichier : {filename}\n\nCode :\n{code}"
    summary = call_model(
        "Tu es un assistant pour développeurs. Tu résumes le code de façon claire.",
        f"Résume ce fichier pour un développeur qui découvre le projet.\n\n{base_prompt}",
    )
    risks = call_model(
        "Tu es un reviewer de code senior.",
        f"Liste les principaux risques, faiblesses ou points d'attention de ce code.\n\n{base_prompt}",
    )
    suggestions = call_model(
        "Tu es un tech lead pragmatique.",
        f"Propose 3 à 5 améliorations concrètes et réalisables rapidement pour ce code.\n\n{base_prompt}",
    )
    return {
        "summary": summary,
        "risks": risks,
        "suggestions": suggestions,
    }


def generate_onboarding(project_description: str, files: List[str]) -> str:
    files_str = "\n".join(f"- {f}" for f in files)
    prompt = f"""Tu aides à on-boarder un développeur sur un projet.

Contexte projet :
{project_description}

Fichiers clés :
{files_str}

Produis :
- Une vue d'ensemble simple (2-3 paragraphes)
- Les 3 premières choses à faire pour prendre en main le projet
- Les questions à poser à l'équipe si quelque chose n'est pas clair
"""
    return call_model(
        "Tu es un lead dev qui fait un plan d'onboarding pour un nouveau développeur.",
        prompt,
    )


def main():
    st.set_page_config(
        page_title="IA Dev Productivity Sandbox",
        layout="wide",
    )

    st.title("🧪 IA Dev Productivity Sandbox")
    st.write(
        "Un petit terrain de jeu pour explorer comment l'IA peut aider les développeurs "
        "sur un projet existant : analyse de fichiers, suggestions d'amélioration, onboarding..."
    )

        # Sidebar : configuration
    st.sidebar.header("⚙️ Configuration")

    # Saisie éventuelle de la clé API
    with st.sidebar.expander("🔑 Clé OpenAI API", expanded=False):
        st.write(
            "Tu peux soit définir la variable d'environnement `OPENAI_API_KEY`, "
            "soit saisir ta clé ici (elle restera en mémoire le temps de la session)."
        )

        api_key_input = st.text_input(
            "Clé OpenAI API",
            type="password",
            placeholder="sk-...",
            help="Elle n'est pas enregistrée côté serveur, uniquement en session.",
        )

        if st.button("Enregistrer la clé API"):
            if api_key_input.strip():
                st.session_state["openai_api_key"] = api_key_input.strip()
                st.success("Clé API enregistrée pour cette session.")
            else:
                st.warning("La clé saisie est vide.")

        # Indicateur d'état : on demande à config quelle clé serait utilisée
        effective_key = get_api_key(get_session_api_key())
        if effective_key:
            st.caption("✅ Une clé OpenAI API est configurée.")
        else:
            st.caption("❌ Aucune clé API détectée pour l'instant.")


    project_name = st.sidebar.text_input("Nom du projet", "Projet démo")
    project_desc = st.sidebar.text_area(
        "Description rapide du projet",
        "Application web avec une API et une base de données, code en Python.",
        height=100,
    )

    st.sidebar.markdown("---")
    st.sidebar.caption(
        "Ce sandbox est un projet pédagogique pour explorer l'IA appliquée au développement."
    )

    tab_analyze, tab_onboarding, tab_checklist = st.tabs(
        ["📄 Analyse de fichier", "🚀 Onboarding dev", "✅ Checklist qualité"]
    )

    # --------- Onglet 1 : Analyse de fichier ----------
    with tab_analyze:
        st.subheader("Analyse d'un fichier de code")
        uploaded_file = st.file_uploader(
            "Charge un fichier source (Python, JS, etc.)",
            type=["py", "js", "ts", "tsx", "jsx", "java", "cs"],
        )

        manual_code = st.text_area(
            "…ou colle du code directement ici",
            height=200,
        )

        col1, col2 = st.columns(2)
        with col1:
            default_filename = "code_paste.py" if manual_code and not uploaded_file else ""
            filename = st.text_input(
                "Nom du fichier (pour le contexte)",
                value=uploaded_file.name if uploaded_file else default_filename,
            )
        with col2:
            run_analysis = st.button("Analyser avec l'IA")

        if run_analysis:
            if not (uploaded_file or manual_code.strip()):
                st.warning("Ajoute un fichier ou colle du code pour lancer l'analyse.")
            else:
                if uploaded_file is not None:
                    code_bytes = uploaded_file.read()
                    try:
                        code = code_bytes.decode("utf-8")
                    except UnicodeDecodeError:
                        st.error("Impossible de décoder le fichier (UTF-8).")
                        code = ""
                else:
                    code = manual_code

                if code:
                    with st.spinner("Analyse en cours…"):
                        result = analyze_code(filename or "fichier_sans_nom", code)

                    st.success("Analyse terminée.")
                    st.markdown("### 📝 Résumé")
                    st.write(result["summary"])

                    st.markdown("### ⚠️ Points d'attention")
                    st.write(result["risks"])

                    st.markdown("### 💡 Pistes d'amélioration")
                    st.write(result["suggestions"])

    # --------- Onglet 2 : Onboarding dev ----------
    with tab_onboarding:
        st.subheader("Générer un plan d'onboarding développeur")
        st.write(
            "Liste quelques fichiers / modules importants du projet (ex: `api/users.py`, `models/order.py`, `frontend/src/App.tsx`)."
        )

        files_input = st.text_area(
            "Fichiers clés du projet (un par ligne)",
            "api/users.py\nmodels/order.py\nfrontend/src/App.tsx",
            height=120,
        )

        if st.button("Générer le plan d'onboarding"):
            files = [f.strip() for f in files_input.splitlines() if f.strip()]
            if not files:
                st.warning("Ajoute au moins un fichier clé.")
            else:
                with st.spinner("Génération du plan d'onboarding…"):
                    onboarding_text = generate_onboarding(project_desc, files)

                st.success("Plan d'onboarding généré.")
                st.markdown("### 📚 Plan d'onboarding proposé")
                st.write(onboarding_text)

    # --------- Onglet 3 : Checklist ----------
    with tab_checklist:
        st.subheader("Checklist qualité / architecture")
        st.write(
            "Génère une checklist à partir du contexte projet. Tu peux l'utiliser pour des revues techniques ou des migrations."
        )

        checklist_focus = st.selectbox(
            "Type de checklist",
            [
                "Revue générale de code",
                "Préparation à une migration (monolithe → API-first)",
                "Qualité & dette technique",
                "Sécurité & authentification",
            ],
        )

        if st.button("Générer la checklist"):
            prompt = f"""Contexte projet :
{project_desc}

Type de checklist souhaitée : {checklist_focus}

Produis une checklist opérationnelle, organisée par sections, avec des cases à cocher que l'équipe peut utiliser.
"""
            with st.spinner("Génération de la checklist…"):
                checklist = call_model(
                    "Tu es un architecte logiciel expérimenté. Tu produis des checklists concrètes et actionnables.",
                    prompt,
                )

            st.success("Checklist générée.")
            st.markdown("### ✅ Checklist")
            st.write(checklist)


if __name__ == "__main__":
    main()

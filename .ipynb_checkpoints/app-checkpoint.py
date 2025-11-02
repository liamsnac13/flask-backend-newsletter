import streamlit as st
import requests

# ----------------------- CONFIG GÉNÉRALE -----------------------
st.set_page_config(
    page_title="Newsletter Client",
    layout="wide",
    page_icon="📬"
)

st.markdown(
    "<h1 style='color: #8b40ff; font-family: sans-serif;'>Validation de la Newsletter</h1>",
    unsafe_allow_html=True
)
st.markdown("---")

# ----------------------- SIMULATION DES DONNÉES -----------------------
# En vrai, tu récupèreras ça depuis n8n
data = {
    "titre": "Révolution Numérique : Low/No Code et IA en Marche !",
    "introduction": "Plongée dans l'univers des nouvelles technologies où automatismes, low/no code, et intelligences artificielles redéfinissent les règles du jeu.",
    "paragraphe_1_titre": "Explosion des Intégrations Hybrides",
    "paragraphe_1_contenu": "Les solutions no-code comme Make, Zapier, et Webflow...",
    "paragraphe_2_titre": "L'Ère de l'IA Générative",
    "paragraphe_2_contenu": "L'intelligence artificielle, et notamment ChatGPT...",
    "paragraphe_3_titre": "Nouvelle Gouvernance Technologique",
    "paragraphe_3_contenu": "L'émergence de rôles comme les 'prompt engineers'...",
    "paragraphe_4_titre": "Démocratisation Numérique",
    "paragraphe_4_contenu": "Avec l'avènement du no-code et des API...",
    "paragraphe_5_titre": "Appel à l'Action",
    "paragraphe_5_contenu": "Explorez ces outils et transformations..."
}

# ----------------------- AFFICHAGE PARAGRAPHES + FEEDBACK -----------------------

feedbacks = {}  # dictionnaire pour stocker les retours

# --- TITRE ET INTRODUCTION ---
col1, col2 = st.columns([5, 2])

with col1:
    st.markdown(f"<h2>{data['titre']}</h2>", unsafe_allow_html=True)
    st.write(data['introduction'])

with col2:
    feedback_titre = st.text_area("💬 Feedback sur le titre et l’introduction", key="feedback_intro", height=150)

feedbacks["intro_titre"] = feedback_titre

st.markdown("<div style='margin-top:30px; border-top: 1px solid #444;'></div>", unsafe_allow_html=True)

# -- PRAGRAPHES --
for i in range(1, 6):
    titre = data[f"paragraphe_{i}_titre"]
    contenu = data[f"paragraphe_{i}_contenu"]
    
    col1, col2 = st.columns([5, 2])

    with col1:
        st.markdown(f"<h4>{titre}</h4>", unsafe_allow_html=True)
        st.write(contenu)

    with col2:
        feedback = st.text_area(f"💬 Feedback paragraphe {i}", key=f"feedback_{i}", height=120)
        feedbacks[f"paragraphe_{i}"] = feedback

    st.markdown("<div style='margin-top:30px; border-top: 1px solid #444;'></div>", unsafe_allow_html=True)

st.markdown("---")

# ----------------------- BOUTON GLOBAL -----------------------
if st.button("📩 Envoyer le feedback global"):
    if any(val.strip() for val in feedbacks.values()):
        # Ici tu peux envoyer à n8n via requests.post(url, json=feedbacks)
        # Exemple : requests.post("https://n8n-webhook-url", json=feedbacks)
        st.success("✅ Tous les feedbacks ont été envoyés, attends un peu avant de voir la version finale !")
    else:
        st.success("✅ Aucun commentaire ajouté. Validation simple envoyée.")

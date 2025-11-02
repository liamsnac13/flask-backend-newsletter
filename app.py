import streamlit as st
import requests

# ⚠️ À METTRE EN PREMIER
st.set_page_config(
    page_title="Newsletter Client",
    layout="wide",
    page_icon="📬"
)

st.title("Validation de la Newsletter")

# --- Bouton pour recharger la dernière newsletter ---
if st.button("🔄 Recharger la dernière newsletter"):
    st.experimental_rerun()

# --- Appel au backend hébergé sur Railway ---
try:
    res = requests.get("https://web-production-54730.up.railway.app/newsletter", timeout=5)

    if res.status_code == 200:
        data = res.json()
    else:
        st.error(f"❌ Le backend a répondu avec le statut : {res.status_code}")
        st.stop()
except requests.exceptions.RequestException as e:
    st.error(f"❌ Erreur de connexion au backend : {e}")
    st.stop()

# --- Initialisation du dictionnaire pour stocker les feedbacks ---
feedbacks = {}

# --- Affichage titre + introduction ---
col1, col2 = st.columns([5, 2])

with col1:
    st.subheader(data.get("titre", ""))
    st.write(data.get("introduction", ""))

with col2:
    feedback_intro = st.text_area("💬 Feedback sur le titre et l’introduction", key="feedback_intro")
    feedbacks["intro_titre"] = feedback_intro

st.markdown("---")

# --- Affichage des paragraphes 1 à 5 dynamiquement ---
for i in range(1, 6):
    titre = data.get(f"paragraphe_{i}_titre", "")
    contenu = data.get(f"paragraphe_{i}_contenu", "")

    col1, col2 = st.columns([5, 2])

    with col1:
        st.markdown(f"#### {titre}")
        st.write(contenu)

    with col2:
        feedback = st.text_area(f"💬 Feedback paragraphe {i}", key=f"feedback_{i}")
        feedbacks[f"paragraphe_{i}"] = feedback

    st.markdown("---")

# --- Bouton global d’envoi des feedbacks ---
st.markdown("## ✅ Envoi final")

if st.button("📩 Envoyer le feedback global"):
    if any(val.strip() for val in feedbacks.values()):
        try:
            # ➤ Webhook n8n réel que tu utilises
            n8n_webhook = "https://n8n.liambackup.online/webhook/newsletter-feedback"

            response = requests.post(n8n_webhook, json=feedbacks)

            if response.status_code == 200:
                st.success("✅ Feedback envoyé avec succès à n8n !")
            else:
                st.warning(f"⚠️ Envoi échoué (status code {response.status_code})")
        except Exception as e:
            st.error(f"❌ Problème de connexion à n8n : {e}")
    else:
        st.info("📝 Aucun feedback saisi, rien à envoyer.")

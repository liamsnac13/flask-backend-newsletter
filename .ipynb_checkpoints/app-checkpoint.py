import streamlit as st
import requests

# ----------------------- CONFIG GÉNÉRALE -----------------------
st.set_page_config(
    page_title="Newsletter Client",
    layout="wide",
    page_icon="📬"
)

# ----------------------- BOUTON RECHARGER -----------------------
if st.button("🔄 Recharger la dernière newsletter"):
    st.rerun()

st.markdown(
    "<h1 style='color: #8b40ff; font-family: sans-serif;'>Validation de la Newsletter</h1>",
    unsafe_allow_html=True
)
st.markdown("---")

# ----------------------- CHARGEMENT DES DONNÉES -----------------------
try:
    res = requests.get("https://web-production-54730.up.railway.app/newsletter")
    if res.status_code == 200:
        data = res.json()[0]["output"]  
    else:
        st.error("❌ Impossible de charger la newsletter.")
        st.stop()
except Exception as e:
    st.error(f"❌ Erreur de connexion : {e}")
    st.stop()

# ----------------------- STOCKAGE DU FEEDBACK -----------------------
feedbacks = {}

# ---------------- TITRE + INTRODUCTION ----------------
col1, col2 = st.columns([5, 2])

with col1:
    st.markdown(f"<h2>{data.get('titre', '')}</h2>", unsafe_allow_html=True)
    st.write(data.get("introduction", ""))

with col2:
    feedback_intro = st.text_area("💬 Feedback sur le titre et l’introduction", key="feedback_intro", height=150)
    feedbacks["intro_titre"] = feedback_intro

st.markdown("<hr style='margin:30px 0;'>", unsafe_allow_html=True)

# ---------------- PARAGRAPHES DYNAMIQUES ----------------
for i in range(1, 6):
    titre_key = f"paragraphe_{i}_titre"
    contenu_key = f"paragraphe_{i}_contenu"

    if titre_key in data and contenu_key in data:
        col1, col2 = st.columns([5, 2])

        with col1:
            st.markdown(f"<h4>{data[titre_key]}</h4>", unsafe_allow_html=True)
            st.write(data[contenu_key])

        with col2:
            feedback = st.text_area(f"💬 Feedback paragraphe {i}", key=f"feedback_{i}", height=120)
            feedbacks[f"paragraphe_{i}"] = feedback

        st.markdown("<hr style='margin:30px 0;'>", unsafe_allow_html=True)

# ----------------------- ENVOI FINAL -----------------------
st.markdown("## ✅ Envoi global")

if st.button("📩 Envoyer le feedback global"):
    if any(val.strip() for val in feedbacks.values()):
        n8n_webhook = "https://n8n-your-url.com/webhook/newsletter-feedback"  # <-- remplace par le tien

        try:
            response = requests.post(n8n_webhook, json=feedbacks)
            if response.status_code == 200:
                st.success("✅ Feedback envoyé avec succès à n8n !")
            else:
                st.warning("⚠️ Problème lors de l'envoi vers n8n.")
        except Exception as e:
            st.error(f"❌ Erreur lors de l'envoi : {e}")
    else:
        st.success("✅ Aucun commentaire ajouté. Validation simple envoyée.")

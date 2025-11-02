import streamlit as st
import requests

# ⚠️ Toujours placer cette ligne en tout premier
st.set_page_config(
    page_title="Newsletter Client",
    layout="wide",
    page_icon="📬"
)

# 🔁 Rechargement manuel
if st.button("🔄 Recharger la dernière newsletter"):
    st.rerun()

# 🎨 Titre principal
st.markdown(
    "<h1 style='color: #8b40ff; font-family: sans-serif;'>Validation de la Newsletter</h1>",
    unsafe_allow_html=True
)
st.markdown("---")

# 📥 Requête au backend Railway
try:
    res = requests.get("https://web-production-54730.up.railway.app/newsletter")
    if res.status_code == 200:
        data = res.json()
    else:
        st.error("❌ Impossible de charger la newsletter.")
        st.stop()
except Exception as e:
    st.error(f"❌ Erreur de connexion : {e}")
    st.stop()

# 📬 Dictionnaire pour stocker tous les feedbacks
feedbacks = {}

# 🔠 Titre + intro
col1, col2 = st.columns([5, 2])

with col1:
    st.markdown(f"<h2>{data.get('titre', '')}</h2>", unsafe_allow_html=True)
    st.write(data.get('introduction', ''))

with col2:
    feedback_intro = st.text_area("💬 Feedback sur le titre et l’introduction", key="feedback_intro", height=150)
    feedbacks["intro_titre"] = feedback_intro

st.markdown("<div style='margin-top:30px; border-top: 1px solid #444;'></div>", unsafe_allow_html=True)

# 📚 Paragraphes 1 à 5
for i in range(1, 6):
    titre = data.get(f"paragraphe_{i}_titre", "")
    contenu = data.get(f"paragraphe_{i}_contenu", "")

    col1, col2 = st.columns([5, 2])
    with col1:
        st.markdown(f"<h4>{titre}</h4>", unsafe_allow_html=True)
        st.write(contenu)

    with col2:
        feedback = st.text_area(f"💬 Feedback paragraphe {i}", key=f"feedback_{i}", height=120)
        feedbacks[f"paragraphe_{i}"] = feedback

    st.markdown("<div style='margin-top:30px; border-top: 1px solid #444;'></div>", unsafe_allow_html=True)

# ✅ BOUTON FINAL
st.markdown("---")
st.markdown("## ✅ Envoi final")

if st.button("📩 Envoyer le feedback global"):
    if any(val.strip() for val in feedbacks.values()):
        # Remplace ceci par ton vrai webhook n8n si tu en as un
        n8n_webhook = "https://n8n-your-webhook-url.com/webhook/newsletter-feedback"

        try:
            response = requests.post(n8n_webhook, json=feedbacks)
            if response.status_code == 200:
                st.success("✅ Feedback envoyé avec succès à n8n !")
            else:
                st.warning("⚠️ Problème lors de l'envoi vers n8n.")
        except Exception as e:
            st.error(f"❌ Erreur lors de l'envoi : {e}")
    else:
        st.info("📝 Aucun feedback saisi, rien à envoyer.")

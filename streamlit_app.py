
import streamlit as st
from datetime import datetime
import requests
from PIL import Image
import io
import dropbox

# Token de Dropbox (debes mantenerlo en secreto)
DROPBOX_TOKEN = "sl.u.AFu1ZSyOeAxdy-K-B82_X3JBsQACtNXrNEJpXfQh0RaR3dVFCl3eMzZRJ5kjUEDmDKIB4pJCZGWeZry_ByYbF6Lrt8F8LTVoD--mMcQ72QbKnzWqWiwaOLl9SHT4PR-Fe3Kgb7j-QaiyM7MhPR9UGQ6yC2DNQs9eSVTc15grKOG3xhM8LxTsY-olGvhPhiFw2EUF5ev3APJpQRA0pIYHnKZWyxxGGHKx6k8hZ88oXesrdsEiYgUDe31_UtDIsFjL3gFk8y0TL-kU0ODirdMJgqlI2c2BPC86dq3J95QtxRLD2bMFKYKQjyywu4wa0O4JTXjbuR-YKiQWm0M9jRMcEh6Z5n60OTR694krX7NKQXXwnQVX29EtUXpX7NS_chFpFQuBR2xQu5pAebgtJ6TwQYIUXMe5VJ_8AJNakLsjQcrdPuxVgADW-xQoSUuEGbcbdvS7b0jBJhAJ9OVAyabHTHGfXvNtfA1RzuEGjeu3qKcNymZU1BpJkAriDo_L7vtQg28YRUKYBYjdovngar4dXXsdAWS324JtDrXa0Fi3yM5Ye4ngbMmsIY4F9VeT1QZJ9B7W4ltYkDBnZgdx1y9L0-5F2eCga-R6l9tA3W8r3UtkWNuilINznQx69mVTuSYkIPTP7kMbwqeVBinVpsbpv3S8u0B0-fS0_2WqV9xfmJcve-nKZt3GOQhFjNpk2Xo4UnZZB0m0hI39Olavs6ZrWm8fOGcbX9XO4oipnMDgalC7dYLlTtLZ6z0sdgRSFPlckpn7zmTT3AH7-e0Njq3vnch1jOqsSn_rC0ah235B81pPp5pwzjECGnndKkRQqvza9ZmDMT4cOj01MgA7BP7WtdpBkOMk2MuFWRtswXbENtSvh-lfyS0fGn_Mv4OfpBZsmA6ciZvJfNtyw0WkwpDeDKQGHN43PBKBocW1Q1l8bZ0hNL9zeWvjvBKcF79qp29D9l22PTUz808O6xOwBZSvIg3D4ifjjth45juwsWtsaC7bGtGJZ2aEGZknq41Q1oKCLY7YE-cV5UCseco1pbATca_92DDmJWmKHX54osUgLaYO4_KMIdYpASSEv1MCDsAOznofuZKXNyuLQoy0Mqhd88g8N0BV1_X-1dW1PzFfehPY8wKe2tHQEsOYm1qi2dfMAuhrQ2GkqwfVXaxfbBGrYUMt7KV_d9mj0vQYaB7Xj8zxr7Xoj-AgaUt1Dykny9RnxY23cFvtZCXtwrSVgfL8hYKIKQUcBPGM0mO9dpXPePoy2_qKZEu_6sr9YQ87bKki0jHowA_KPaDeYeCDx4pqxrtv-9B5QknPJSwAIQ1IIKMz6w10PT9NLIam57s7ZS6vwMk"

st.set_page_config(page_title="Subida de Albaranes", layout="centered")

st.markdown("""
    <style>
    body, .stApp { background-color: white; }
    .logo-container { text-align: center; margin-top: 20px; }
    .logo-container img { width: 350px; }
    label { color: black !important; font-weight: bold; }
    input:focus { border: 2px solid #f7941d !important; box-shadow: 0 0 0 0.1rem rgba(247, 148, 29, 0.3) !important; }
    .stButton > button {
        background-color: #f7941d; color: white; font-weight: bold;
        border-radius: 6px; height: 2.5em; width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Logo
st.markdown('<div class="logo-container"><img src="static/logo.png"></div>', unsafe_allow_html=True)

# Subida y OCR
uploaded_file = st.file_uploader("Sube el albarán", type=["jpg", "jpeg", "png"])
proveedor = fecha = cliente = ""

if uploaded_file:
    image_bytes = uploaded_file.read()
    try:
        response = requests.post("https://ocr.mantotal.app/ocr", files={"file": image_bytes})
        response.raise_for_status()
        data = response.json()
        proveedor = data.get("proveedor", "")
        fecha = data.get("fecha", "")
        cliente = data.get("cliente", "")
    except:
        st.warning("Error en el OCR. Rellena los datos manualmente.")

# Inputs
proveedor = st.text_input("Proveedor", value=proveedor)
fecha_raw = st.text_input("Fecha", value=fecha)
cliente = st.text_input("Cliente/Referencia", value=cliente)

# Confirmación
if st.button("Confirmar") and uploaded_file:
    try:
        fecha_fmt = datetime.strptime(fecha_raw, "%Y-%m-%d").strftime("%y%m%d")
    except:
        fecha_fmt = fecha_raw
    nuevo_nombre = f"{proveedor}-{fecha_fmt}-{cliente}.pdf"

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    pdf_bytes = io.BytesIO()
    image.save(pdf_bytes, format="PDF")
    pdf_bytes.seek(0)

    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    dbx.files_upload(pdf_bytes.read(), f"/{nuevo_nombre}", mode=dropbox.files.WriteMode("overwrite"))

    st.success(f"Archivo subido como {nuevo_nombre}")

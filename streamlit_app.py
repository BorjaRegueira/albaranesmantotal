import streamlit as st
import requests
from PIL import Image
import io
import base64
from datetime import datetime

st.set_page_config(layout="centered")

# Logo centrado
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/BorjaRegueira/albaranesmantotal/main/static/logo.png" width="175">
    </div>
    """,
    unsafe_allow_html=True
)

# Contenedor principal
st.markdown(
    """
    <div style="background-color: #fff6ea; border: 2px solid #f7941d; border-radius: 10px; padding: 1.5em; margin: 1em auto; max-width: 600px;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h4 style="color: #f7941d; margin: 0;">Suelta el albarán aquí</h4>
                <p style="margin: 0; color: #333;">o explora archivos</p>
            </div>
            <div>
                <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="#f7941d" viewBox="0 0 16 16">
                  <path d="M.5 9.9A.5.5 0 0 1 1 9.5h14a.5.5 0 0 1 .5.4v4.6a.5.5 0 0 1-.5.5H1a.5.5 0 0 1-.5-.5V9.9zm7.5-.5 4-4H9V1.5a.5.5 0 0 0-1 0V5.4H5l4 4z"/>
                </svg>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Subida de archivo
uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

proveedor = ""
fecha = ""
cliente = ""

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
        st.warning("Error conectando al OCR. Rellena manualmente.")

# Vista previa
st.markdown("<h6 style='text-align: center;'>Vista previa del albarán</h6>", unsafe_allow_html=True)

css = """
<style>
    label {
        color: black !important;
        font-weight: 500;
    }
    input:focus {
        border: 2px solid #f7941d !important;
        box-shadow: 0 0 0 0.1rem rgba(247, 148, 29, 0.3) !important;
    }
</style>
"""

st.markdown(css, unsafe_allow_html=True)

col1, col2 = st.columns(2)

proveedor = st.text_input("Proveedor", value=proveedor)
col1, col2 = st.columns(2)
fecha = col1.text_input("Fecha", value=fecha)
cliente = col2.text_input("Cliente/Referencia", value=cliente)

# Botón de confirmar
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #f7941d;
        color: white;
        font-weight: bold;
        width: 100%;
        padding: 10px;
        border: none;
        border-radius: 5px;
        margin-top: 1em;
    }
    div.stButton > button:hover {
        background-color: #e07a00;
    }
    </style>
""", unsafe_allow_html=True)

if st.button("Confirmar"):
    st.success(f"Subido: {proveedor}-{fecha}-{cliente}")

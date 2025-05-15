import streamlit as st
import requests
import datetime
import base64
import dropbox
from io import BytesIO
from PIL import Image

# ---------- CONFIGURACIÓN DE PÁGINA ----------
st.set_page_config(page_title="Subida de Albaranes", layout="centered")

# ---------- ESTILOS PERSONALIZADOS ----------
st.markdown("""
    <style>
    body, .main, .stApp {
        background-color: white;
        color: black;
        font-family: 'Arial', sans-serif;
    }
    .custom-upload {
        background-color: #fff5e6;
        border: 2px solid #f7941d;
        border-radius: 10px;
        padding: 2em;
        margin-bottom: 2em;
        position: relative;
    }
    .custom-upload h3 {
        color: #f7941d;
        font-size: 1.3em;
        margin-bottom: 0.3em;
        font-weight: bold;
    }
    .custom-upload small {
        color: #333;
    }
    .stTextInput>div>div>input {
        background-color: white;
        border: 1px solid black;
        color: black;
        border-radius: 5px;
    }
    .stTextInput>div>div>input:focus {
        border: 2px solid #f7941d;
    }
    .stButton>button {
        background-color: #f7941d;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
        width: 100%;
    }
    img.logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 350px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- LOGO ----------
st.markdown("<img src='https://raw.githubusercontent.com/BorjaRegueira/albaranesmantotal/main/static/logo.png' class='logo'>", unsafe_allow_html=True)

st.write("## Sube el albarán")
archivo = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

proveedor = ""
fecha = ""
cliente = ""

# ---------- EXTRACCIÓN OCR ----------
if archivo is not None:
    image = Image.open(archivo)
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_bytes = buffered.getvalue()

    try:
        response = requests.post(
            "https://ocr.mantotal.app/extraer",
            files={"image": img_bytes}
        )
        response.raise_for_status()
        data = response.json()
        proveedor = data.get("proveedor", "")
        fecha = data.get("fecha", "")
        cliente = data.get("cliente", "")
    except:
        st.warning("Error en el OCR. Rellena los datos manualmente.")

# ---------- CAMPOS DE TEXTO ----------
proveedor_input = st.text_input("Proveedor", value=proveedor)
fecha_input = st.text_input("Fecha", value=fecha)
cliente_input = st.text_input("Cliente/Referencia", value=cliente)

# ---------- ENVÍO ----------
if st.button("Confirmar"):
    if not (proveedor_input and fecha_input and cliente_input):
        st.error("Por favor, completa todos los campos antes de confirmar.")
    elif archivo is None:
        st.error("Debes subir un archivo antes de confirmar.")
    else:
        # Procesar archivo: renombrar y subir a Dropbox
        nombre_archivo = f"{proveedor_input.strip().upper()}-{fecha_input.strip()}-{cliente_input.strip().upper()}.pdf"

        # Convertir imagen a PDF
        img = Image.open(archivo).convert("RGB")
        buffer_pdf = BytesIO()
        img.save(buffer_pdf, format="PDF")
        buffer_pdf.seek(0)

        # Subir a Dropbox
        try:
            dbx = dropbox.Dropbox(st.secrets["DROPBOX_TOKEN"])
            dbx.files_upload(buffer_pdf.read(), f"/Albaranes/{nombre_archivo}", mode=dropbox.files.WriteMode.overwrite)
            st.success(f"Albarán subido correctamente como {nombre_archivo}")
        except Exception as e:
            st.error(f"Error subiendo a Dropbox: {e}")

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
proveedor_input = st.markdown("<span style=\"color: black; font-weight: bold;\">Proveedor</span>", unsafe_allow_html=True)
proveedor_input = st.text_input("Proveedor", value=proveedor, label_visibility="visible")
fecha_input = st.markdown("<span style=\"color: black; font-weight: bold;\">Fecha</span>", unsafe_allow_html=True)
fecha_input = st.text_input("Fecha", value=fecha, label_visibility="visible")
cliente_input = st.markdown("<span style=\"color: black; font-weight: bold;\">Cliente/Referencia</span>", unsafe_allow_html=True)
cliente_input = st.text_input("Cliente", value=cliente, label_visibility="visible")

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
            dbx = dropbox.Dropbox(st.secrets["sl.u.AFufdcDQVnhoorOHxGUQSBXG8aW4sy4LhPBGpC0bcCjGU817IQyFDQZUFoRkA0FDVruQu6M_d8gfou94yYA2z5vOShrfuHThvoC9sin9eAhlgA9jIOP0CaoT3_y_4rjaxZEqbkfi3g4sa91FDKi-yWgKFW5lQH8ifogyCUKOmkNvbsyER7hlIT_Daaxy0XaKGOMfUzQ9Av4nNpsnSiOnvzZQ97K0EjkSNnVwampzlEg7NkGA1IRGqC6PmM-EftJnlSr5mpUD8m3MvLJkrFaZ4JlQoGIU96Wnb3OE5Zyxsxv0GS4XCNUTD-n-BmwxtlK7yubEdWWtAYylj1d5PomXdg6dk_sFATnkKeC0fIlJnaVTc6UpuKsFhV2HIfnrwaejcwGu0XVrWNcutuZ4SrQVKmieKmZcfo9OLv_o893rqIeN9hPnnGMhvF5KdXM_eh1BtrMdhyfam4SX9e0UeyZ-0_MknUgGtDPzZAU91aQ6adzPFthvG5awvtcT_F4ebvlfG5waCnllwCs5CKLaf6FUtikXpkm5XJwoVAGFgPHq-DkS5O1VId9VspjWy_RgugamJi59vM0lbOWeCkZuFM0hefqyDGpxrur1g1Jh8yChHkXDToJm723GAfw5w9wgT_h5SaA3Jn2LGE53YkLNXf2lUfBkxgJAV0k55WfYzeykspBfqfv5jMB7IUTAeActIk2T_uvSukNoOwB0Y0fkGJPurBaiYqJYVnKa9myQir8aSMsCKLE0KmBRdKjq5ocvXOFxl4XWr6CCytk7C1TObCOvCl8LDdsjMN0udEV06waE_hhAQQ17Qq74p0WwyRcS7jGl5t9xmg4ti6A8b4OR95e8coUxxbAOjiCrJUcGOzrzXVnf7H8GCVWnTgKDIIPwuSort9QjVJwW-X-iObWQRSOptiwjxVKFuF-L4mZajVAtMIQ1W_Jvk30V5z0fI-FgWAQxGAtXGCsXIbZ1YqLgDd2AIFpwvhqBdHY8XxhGB69U_D4Np_wLl6Tf5BzP8wjHsUKYfm7v9HZzKg4OYvrx6w8vcCmJHgKH4cXJqkxB4Vc6guSa2GfEUsH661z3du4x721_s7NxqR1u6_-702iCOxF0sB5zTLfXPdvhIquCznRykFE9CDoOqygDi1v6ZtNORxQokJHFGPCSzZRT0qs0XaFhPuxhjM2Y2euaQfyrKnHDlIAwwyO0wKddePNPaZ1h_3zmeqDJ8MekuS82aPgv101f-_mEH5DbXKg1Jm40Hjn-jLy-oq5z_nub00zz-zvdgIhBRYsnHu7QVtL0m8woauDVR_03Dcvy4z4qX695LT0swhKzblwIF12g9uq8THT_dXUh6Pw"])
            dbx.files_upload(buffer_pdf.read(), f"/Albaranes/{nombre_archivo}", mode=dropbox.files.WriteMode.overwrite)
            st.success(f"Albarán subido correctamente como {nombre_archivo}")
        except Exception as e:
            st.error(f"Error subiendo a Dropbox: {e}")

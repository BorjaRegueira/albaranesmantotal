import streamlit as st
from datetime import datetime
from PIL import Image
import requests
import dropbox
import os
import io

# --- CONFIGURACIÓN ---
DROPBOX_TOKEN = "sl.u.AFufdcDQVnhoorOHxGUQSBXG8aW4sy4LhPBGpC0bcCjGU817IQyFDQZUFoRkA0FDVruQu6M_d8gfou94yYA2z5vOShrfuHThvoC9sin9eAhlgA9jIOP0CaoT3_y_4rjaxZEqbkfi3g4sa91FDKi-yWgKFW5lQH8ifogyCUKOmkNvbsyER7hlIT_Daaxy0XaKGOMfUzQ9Av4nNpsnSiOnvzZQ97K0EjkSNnVwampzlEg7NkGA1IRGqC6PmM-EftJnlSr5mpUD8m3MvLJkrFaZ4JlQoGIU96Wnb3OE5Zyxsxv0GS4XCNUTD-n-BmwxtlK7yubEdWWtAYylj1d5PomXdg6dk_sFATnkKeC0fIlJnaVTc6UpuKsFhV2HIfnrwaejcwGu0XVrWNcutuZ4SrQVKmieKmZcfo9OLv_o893rqIeN9hPnnGMhvF5KdXM_eh1BtrMdhyfam4SX9e0UeyZ-0_MknUgGtDPzZAU91aQ6adzPFthvG5awvtcT_F4ebvlfG5waCnllwCs5CKLaf6FUtikXpkm5XJwoVAGFgPHq-DkS5O1VId9VspjWy_RgugamJi59vM0lbOWeCkZuFM0hefqyDGpxrur1g1Jh8yChHkXDToJm723GAfw5w9wgT_h5SaA3Jn2LGE53YkLNXf2lUfBkxgJAV0k55WfYzeykspBfqfv5jMB7IUTAeActIk2T_uvSukNoOwB0Y0fkGJPurBaiYqJYVnKa9myQir8aSMsCKLE0KmBRdKjq5ocvXOFxl4XWr6CCytk7C1TObCOvCl8LDdsjMN0udEV06waE_hhAQQ17Qq74p0WwyRcS7jGl5t9xmg4ti6A8b4OR95e8coUxxbAOjiCrJUcGOzrzXVnf7H8GCVWnTgKDIIPwuSort9QjVJwW-X-iObWQRSOptiwjxVKFuF-L4mZajVAtMIQ1W_Jvk30V5z0fI-FgWAQxGAtXGCsXIbZ1YqLgDd2AIFpwvhqBdHY8XxhGB69U_D4Np_wLl6Tf5BzP8wjHsUKYfm7v9HZzKg4OYvrx6w8vcCmJHgKH4cXJqkxB4Vc6guSa2GfEUsH661z3du4x721_s7NxqR1u6_-702iCOxF0sB5zTLfXPdvhIquCznRykFE9CDoOqygDi1v6ZtNORxQokJHFGPCSzZRT0qs0XaFhPuxhjM2Y2euaQfyrKnHDlIAwwyO0wKddePNPaZ1h_3zmeqDJ8MekuS82aPgv101f-_mEH5DbXKg1Jm40Hjn-jLy-oq5z_nub00zz-zvdgIhBRYsnHu7QVtL0m8woauDVR_03Dcvy4z4qX695LT0swhKzblwIF12g9uq8THT_dXUh6Pw"
DROPBOX_CARPETA = ""
OCR_URL = "https://ocr.mantotal.app/extraer"

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Subida de Albaranes", layout="centered")
st.markdown("""
    <style>
        body, .main, .stApp {
            background-color: white;
            color: black;
            font-family: 'Arial', sans-serif;
        }
        .main-container {
            max-width: 500px;
            margin: auto;
            background-color: white;
            border-radius: 10px;
            padding: 20px;
        }
        .file-drop-box {
            border: 2px solid #f7941d;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            font-weight: bold;
            color: #f7941d;
            background-color: #fff9f2;
            margin-bottom: 20px;
        }
        .stTextInput>div>div>input,
        .stDateInput>div>input {
            background-color: white;
            border: 2px solid black;
            color: black;
        }
        .stTextInput>div>div>input:focus,
        .stDateInput>div>input:focus {
            border-color: #f7941d;
            outline: none;
            box-shadow: 0 0 0 0.1rem rgba(247, 148, 29, 0.25);
        }
        .stButton>button {
            background-color: #f7941d;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75em 2em;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #e6821b;
        }
    </style>
""", unsafe_allow_html=True)

st.image("static/logo.png", width=220)
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

st.markdown("<div class='file-drop-box'>Suelta el albarán aquí<br><span style='font-weight: normal; font-size: 0.9em;'>o explora archivos</span></div>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

proveedor = ""
fecha = ""
texto_error = ""

if uploaded_file is not None:
    st.image(uploaded_file, caption="Vista previa del albarán", use_column_width=True)
    with st.spinner("Analizando albarán..."):
        try:
            response = requests.post(
                OCR_URL,
                files={"file": (uploaded_file.name, uploaded_file, uploaded_file.type)},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                proveedor = data.get("proveedor", "")
                fecha = data.get("fecha", "")
            else:
                texto_error = "No se pudo procesar la imagen. Rellene manualmente."
        except Exception:
            texto_error = "Error conectando al OCR. Rellene manualmente."

    if texto_error:
        st.warning(texto_error)

    with st.form("confirmar_form"):
        proveedor = st.text_input("Proveedor", value=proveedor)
        col1, col2 = st.columns(2)
        with col1:
            fecha_input = st.date_input("Fecha", value=datetime.today() if not fecha else datetime.strptime(fecha, "%Y-%m-%d"))
        with col2:
            referencias = st.text_input("Cliente/Referencia")
        submitted = st.form_submit_button("Confirmar")

        if submitted:
            with st.spinner("Subiendo archivo a Dropbox..."):
                try:
                    img = Image.open(uploaded_file).convert("RGB")
                    pdf_buffer = io.BytesIO()
                    img.save(pdf_buffer, format="PDF")
                    pdf_buffer.seek(0)

                    fecha_str = fecha_input.strftime("%y%m%d")
                    ref_str = "_".join([r.strip() for r in referencias.split(",")])
                    nombre_archivo = f"{proveedor}-{fecha_str}-{ref_str}.pdf"
                    ruta_dropbox = f"{DROPBOX_CARPETA}/{nombre_archivo}"

                    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
                    dbx.files_upload(pdf_buffer.read(), ruta_dropbox, mode=dropbox.files.WriteMode("overwrite"))

                    st.success(f"✅ Archivo subido correctamente como: {nombre_archivo}")
                except Exception as e:
                    st.error(f"Error al subir a Dropbox: {e}")

st.markdown("</div>", unsafe_allow_html=True)

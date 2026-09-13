# -------------------------------------------------------------
# EJERCICIO – 3
# Autor: Héctor Fernández-Clemente Cicuéndez
# -------------------------------------------------------------

import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io

# =========================================================
# PREGUNTA 1 – CONFIGURACIÓN DEL ENTORNO
# =========================================================
st.set_page_config(page_title="Generador de Credenciales", layout="wide")
st.title("Proyecto Final – Generador de Identidad Corporativa")
st.subheader("Automatización de credenciales con Streamlit + Pillow")

# =========================================================
# PREGUNTA 2 – FORMULARIO DE DATOS DINÁMICOS
# =========================================================
st.header("Captura de Datos")

with st.form("form_datos"):
    nombre = st.text_input("Nombre Completo")
    cargo = st.text_input("Cargo")
    id_empleado = st.text_input("Número de Empleado")
    enviado = st.form_submit_button("Guardar Datos")

if enviado:
    st.success("Datos cargados correctamente.")

# =========================================================
# PREGUNTA 3 – CARGA DE FOTOGRAFÍA
# =========================================================
st.header("Subir Fotografía")

foto_subida = st.file_uploader("Subir foto de perfil", type=["jpg", "jpeg", "png"])

# =========================================================
# PREGUNTA 4 – COLOR PERSONALIZADO DEL BANNER
# =========================================================
st.header("Selección de Color del Banner")

color_banner = st.color_picker("Selecciona el color corporativo", "#007bff")

# =========================================================
# PREGUNTA 5 – VALIDACIÓN DE EJECUCIÓN
# =========================================================
st.header("Validación")

if foto_subida is None:
    st.warning("Sube una fotografía para continuar.")
    st.stop()

# =========================================================
# PREGUNTA 6 – DISTRIBUCIÓN EN PANTALLA
# =========================================================
col1, col2 = st.columns(2)

with col1:
    st.write("### Datos del Empleado")
    st.write(f"**Nombre:** {nombre}")
    st.write(f"**Cargo:** {cargo}")
    st.write(f"**ID:** {id_empleado}")

# =========================================================
# PREGUNTA 7 – SINCRONIZACIÓN DE DATOS Y GENERACIÓN
# =========================================================
# Parámetros del carnet
ANCHO = 400
ALTO = 600

# Crear lienzo
carnet = Image.new("RGB", (ANCHO, ALTO), "white")
draw = ImageDraw.Draw(carnet)

# Cargar fuentes
try:
    font_nombre = ImageFont.truetype("arial.ttf", 35)
    font_cargo = ImageFont.truetype("arial.ttf", 20)
    font_id = ImageFont.truetype("arial.ttf", 16)
    font_footer = ImageFont.truetype("arial.ttf", 12)
except:
    font_nombre = ImageFont.load_default()
    font_cargo = ImageFont.load_default()
    font_id = ImageFont.load_default()
    font_footer = ImageFont.load_default()

# Banner superior
draw.rectangle([0, 0, ANCHO, 180], fill=color_banner)

# Procesar foto circular
foto = Image.open(foto_subida)
foto_perfil = ImageOps.fit(foto, (180, 180), centering=(0.5, 0.5))

mask = Image.new("L", (180, 180), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.ellipse((0, 0, 180, 180), fill=255)

carnet.paste(foto_perfil, (110, 90), mask)

# Textos
draw.text((ANCHO/2, 310), nombre.upper(), font=font_nombre, fill="black", anchor="mm")
draw.text((ANCHO/2, 350), cargo, font=font_cargo, fill="#555555", anchor="mm")
draw.line([120, 380, 280, 380], fill=color_banner, width=3)
draw.text((ANCHO/2, 410), f"ID: {id_empleado}", font=font_id, fill="black", anchor="mm")

# Footer
draw.rectangle([0, ALTO - 60, ANCHO, ALTO], fill="#f8f9fa")
draw.text((ANCHO/2, ALTO - 30), "PROPIEDAD PRIVADA - USO INTERNO", font=font_footer, fill="#adb5bd", anchor="mm")

# =========================================================
# PREGUNTA 8 – VISTA PREVIA INSTANTÁNEA
# =========================================================
with col2:
    st.header("Vista Previa")
    st.image(carnet, caption="Carnet Generado", use_column_width=True)

# =========================================================
# PREGUNTA 9 – PROCESAMIENTO EN MEMORIA
# =========================================================
buffer = io.BytesIO()
carnet.save(buffer, format="PNG")
buffer.seek(0)

# =========================================================
# PREGUNTA 10 – DESCARGA DEL ARCHIVO
# =========================================================
st.download_button(
    label="Descargar Credencial",
    data=buffer,
    file_name=f"credencial_{nombre.replace(' ', '_')}.png",
    mime="image/png"
)

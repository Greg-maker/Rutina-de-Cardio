import os
import re
import time
import unicodedata
from datetime import datetime

import pytz
import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="RUTINA DE CARDIO Y FUERZA", page_icon="🏃‍♂️", layout="centered"
)

# --- ESTILO VISUAL (CSS PERSONALIZADO) ---
st.markdown(
    """
    <style>
    .stMetric { background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
    .stExpander { border: 1px solid #334155; border-radius: 8px; background-color: #0f172a; margin-bottom: 10px; }
    
    div.stButton > button:first-child { 
        background-color: #2563eb; 
        color: white; 
        border: none; 
        font-weight: bold; 
        width: 100%; 
        height: 3em;
        font-size: 1.2em;
        border-radius: 6px;
    }
    div.stButton > button:first-child:hover { background-color: #1d4ed8; }
    .stProgress > div > div > div > div { background-color: #2563eb; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- TIEMPO Y NAVEGACIÓN (TIJUANA) ---
tz = pytz.timezone("America/Tijuana")
hoy_tj = datetime.now(tz)
dias_es = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo",
}
dia_actual = dias_es.get(hoy_tj.strftime("%A"), "Lunes")


# --- LOCALIZADOR DE ARCHIVOS DE VIDEO EN LA RAÍZ ---
def obtener_ruta_local_video(nombre_ejercicio):
    nombre_normalizado = unicodedata.normalize("NFD", nombre_ejercicio)
    nombre_sin_acentos = "".join(
        c for c in nombre_normalizado if unicodedata.category(c) != "MN"
    )

    nombre_limpio = nombre_sin_acentos.lower().strip()
    nombre_limpio = re.sub(r"\s+", "_", nombre_limpio)
    nombre_limpio = re.sub(r"[^a-z0-9_]", "", nombre_limpio)

    ruta_archivo = f"{nombre_limpio}.mp4"

    if os.path.exists(ruta_archivo):
        return ruta_archivo

    return None


# --- FUNCIÓN REUTILIZABLE PARA TEMPORIZADOR ---
def ejecutar_temporizador(segundos, key_btn):
    if st.button(f"✅ CONCLUIR SERIE / EJERCICIO", key=key_btn):
        msg = st.empty()
        bar = st.progress(0)
        for s in range(segundos, -1, -1):
            msg.subheader(f"⏳ Descansando: {s}s")
            bar.progress((segundos - s) / segundos)
            time.sleep(1)
        msg.success("💪 ¡Tiempo cumplido!")
        st.balloons()
        time.sleep(1)


# --- BASE DE DATOS DE RUTINAS (FULL CARDIO Y PESO CORPORAL) ---
rutinas = {
    "Lunes": [
        (
            "Sentadillas",
            "3 × 12 a 15",
            60,
            "Mantén la espalda recta y baja de forma controlada.",
        ),
        (
            "Flexiones de pecho",
            "3 × 8 a 12",
            60,
            "Apoyar rodillas si cuesta llegar a 8 repeticiones.",
        ),
        (
            "Zancadas alternas",
            "3 × 10 (por pierna)",
            60,
            "Paso firme hacia adelante manteniendo el torso erguido.",
        ),
        (
            "Plancha abdominal",
            "3 × 30 a 45 seg",
            45,
            "Mantén la cadera alineada con la espalda y activa el abdomen.",
        ),
    ],
    "Martes": [
        (
            "Jumping Jacks",
            "45 segundos",
            15,
            "Saltos fluidos abriendo y cerrando brazos y piernas simultáneamente.",
        ),
        (
            "Escaladores (Mountain climbers)",
            "30 segundos",
            15,
            "En posición de plancha alta, lleva las rodillas al pecho con ritmo.",
        ),
        (
            "Paso de oso",
            "45 segundos",
            15,
            "Camina en 4 apoyos ida y vuelta manteniendo las rodillas cerca del suelo.",
        ),
        (
            "Skipping",
            "30 segundos",
            60,
            "Correr en el sitio elevando las rodillas a la altura de la cadera. Restan 60s al completar la vuelta del circuito.",
        ),
    ],
    "Miércoles": [],
    "Jueves": [
        (
            "Flexiones de pecho",
            "3 × 8 a 12",
            60,
            "Enfoque en pectorales y tríceps.",
        ),
        (
            "Puente de glúteo",
            "3 × 15",
            45,
            "Acostado boca arriba, eleva la cadera apretando glúteos arriba.",
        ),
        (
            "Fondos de tríceps en silla o sofá",
            "3 × 10 a 12",
            60,
            "Flexiona codos hacia atrás manteniendo el cuerpo cerca de la silla.",
        ),
        (
            "Supermanes (Espalda baja)",
            "3 × 12 a 15",
            45,
            "Boca abajo, eleva pecho y piernas ligeramente del suelo.",
        ),
        (
            "Plancha lateral",
            "3 × 25 seg (por lado)",
            30,
            "Soporte sobre un antebrazo manteniendo el cuerpo alineado.",
        ),
    ],
    "Viernes": [
        (
            "Sentadillas",
            "15 repeticiones",
            20,
            "Ritmo constante y fluido.",
        ),
        (
            "Jumping Jacks",
            "45 segundos",
            20,
            "Mantén la intensidad cardiovascular.",
        ),
        (
            "Zancadas atrás",
            "10 por pierna",
            20,
            "Paso hacia atrás controlando la bajada.",
        ),
        (
            "Plancha abdominal",
            "40 segundos",
            20,
            "Resistencia isométrica central.",
        ),
    ],
    "Sábado": [],
    "Domingo": [],
}

# --- HEADER PRINCIPAL ---
st.title("🏃‍♂️ ENTRENAMIENTO Y CARDIO")
st.write("---")

c_r1, c_r2 = st.columns(2)
with c_r1:
    st.subheader(f"📅 Hoy es {dia_actual}")
with c_r2:
    st.markdown(
        f"<p style='text-align: right; color: #94a3b8;'>{hoy_tj.strftime('%d / %m / %Y')}</p>",
        unsafe_allow_html=True,
    )

# --- SELECCIÓN DE DÍA DIRECTA ---
seleccion_dia = st.selectbox(
    "Selecciona el día de entrenamiento:",
    list(rutinas.keys()),
    index=list(rutinas.keys()).index(dia_actual),
)

ejercicios = rutinas.get(seleccion_dia, [])

if not ejercicios:
    if seleccion_dia == "Miércoles":
        st.info("🛌 Miércoles: Día de descanso y recuperación. Solo caminar o estirar suavemente.")
    else:
        st.info(f"🛌 {seleccion_dia}: Día de descanso. Importante para la recuperación muscular.")
else:
    if seleccion_dia == "Martes":
        st.warning("🔥 **Circuito Cardio en Casa:** Realizar este circuito 4 veces en total, descansando 1 minuto entre cada vuelta completa.")
    elif seleccion_dia == "Viernes":
        st.warning("⚡ **Circuito Quemagrasa (Alta Intensidad):** Completar de 3 a 4 rondas. Pasa de un ejercicio a otro con solo 20 segundos de descanso.")

    st.subheader(f"📋 Ejercicios – {seleccion_dia}")

    # Uso de enumerate() para garantizar llaves únicas por índice
    for idx, (nombre, reps, desc, enfoque) in enumerate(ejercicios):
        nombre_limpio_key = re.sub(r"[^a-z0-9]", "", nombre.lower())
        id_unico = f"btn_{seleccion_dia.lower()}_{idx}_{nombre_limpio_key}"

        with st.expander(f"🤸 {nombre} ➔ {reps}"):
            st.markdown(f"🎯 **Indicación / Técnica:** {enfoque}")
            st.markdown(f"⏱️ **Tiempo de Descanso Sugerido:** {desc} segundos")

            # REPRODUCTOR DE VIDEO LOCAL (.mp4)
            ruta_video = obtener_ruta_local_video(nombre)

            if ruta_video:
                st.video(ruta_video)
            else:
                nombre_limpio_sugerido = (
                    "".join(
                        c
                        for c in unicodedata.normalize("NFD", nombre.lower())
                        if unicodedata.category(c) != "MN"
                    )
                    .replace(" ", "_")
                    .replace("(", "")
                    .replace(")", "")
                    .replace("/", "_")
                )
                st.caption(
                    f"ℹ️ Video no encontrado. Nómbralo como: `{nombre_limpio_sugerido}.mp4` en GitHub."
                )

            st.write("---")

            # TEMPORIZADOR DE DESCANSO CON LLAVE ÚNICA
            ejecutar_temporizador(desc, id_unico)

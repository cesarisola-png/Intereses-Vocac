import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
)

st.set_page_config(page_title="Cuestionario BTSA - Estilos de Pensamiento", layout="centered")

# ----------------------------------------------------------------------
# DATOS DE CADA MODO
# ----------------------------------------------------------------------

MODOS = {
    "Modo I": {
        "ubicacion": "Posterior Izquierdo",
        "parrafo": (
            "El pensamiento del Modo I es como un ritmo estable, donde las cosas funcionan bien "
            "y todo tiene su lugar. A estos tipos les gusta hacer las cosas de la misma manera "
            "siempre, y se sienten buenos haciéndolo. Son super detallistas y les encanta cumplir "
            "con las tareas que tienen, siempre. Les gusta trabajar con reglas claras y no les "
            "gusta improvisar. Son personas serias, fiables y leales, y su trabajo es muy valioso "
            "para otros. Les gustan las cosas como siempre fueron, y no les gusta cambiar.\n\n"
            "En resumen, el Modo I es como un motor bien engrasado, que sigue funcionando sin "
            "problemas siempre. Les gusta la planificación y la orden, y les parece que funciona "
            "mejor de esa manera."
        ),
        "items": [
            "Me encanta tener las cosas ordenadas en mi espacio.",
            "Me gusta ser meticuloso y enfocarme en los detalles.",
            "Me considero una persona responsable y fiable.",
            "Me gusta hacer cosas como organizar mi espacio, planificar mi tiempo y crear listas de tareas.",
            "Creo que es importante seguir las reglas y respetar las normas.",
            "Para trabajar preferiría tener instrucciones claras y seguir un procedimiento específico.",
            "Me considero un poco tradicional y me gusta hacer las cosas de la misma manera siempre.",
            "Me gusta tener un lugar específico para cada cosa en mi casa y en el trabajo.",
            "Me gusta resolver problemas paso a paso y seguir un plan para lograr mis objetivos.",
            "Me molesta la ambigüedad y me gusta tener clara mi dirección en la vida.",
            "Me esfuerzo por entregar mis tareas a tiempo y hacerlas de la mejor manera posible.",
            "Prefiero ser amigo de personas que sean responsables y maduras.",
            "Siempre leo las instrucciones antes de empezar algo nuevo.",
            "Me gusta tener rutinas regulares y mantener una estructura en mi vida.",
            "Me molesta cuando algo sale de la norma y me gusta planificar mis actividades con anticipación.",
        ],
    },
    "Modo II": {
        "ubicacion": "Posterior Derecho",
        "parrafo": (
            "El pensamiento del Modo II es como una conexión emocional con los demás. Puedes "
            "sentir lo que la gente está sintiendo sin que ellos digan nada. Los que tienen este "
            "pensamiento suelen ser muy expresivos y buenos comunicadores. Les gusta ayudar a los "
            "demás y hacer que se sientan bien. Son muy empáticos y se preocupan por cómo se "
            "sienten las personas. Les importa mucho la emoción y el estado de ánimo de los demás, "
            "lo que les ayuda a ser mejores amigos y compañeros de trabajo. Además, tienen una "
            "habilidad natural para motivar a los demás y hacer que se sientan parte de algo "
            "importante."
        ),
        "items": [
            "Me doy cuenta que la forma de actuar de las personas es importante para mí.",
            "Considero que los sentimientos son más reales que los pensamientos.",
            "Me gusta hablar con las personas y escuchar sus problemas.",
            "Me considero una persona muy sensible.",
            "Me relaciono bien con las personas y puedo sentir cómo se sienten.",
            "Me destaco en hacer que las personas estén animadas y motivadas.",
            "A veces toco a las personas para animarlas.",
            "Me fijo en la cara de las personas a las que hablo.",
            "Me encanta la música y bailar.",
            "Creo que es importante seguir creciendo y mejorando.",
            "Me definiría como alguien que busca experiencias positivas en la vida.",
            "Considero que las relaciones con los demás son muy importantes para mí.",
            "Me siento incómodo cuando hay conflicto.",
            "Creo que la gente tiene que trabajar juntos y ser amigable.",
            "Me interesa saber cómo se siente la gente y cómo se relacionan entre sí.",
        ],
    },
    "Modo III": {
        "ubicacion": "Frontal Derecho",
        "parrafo": (
            "La forma de pensar del Modo III es un poco como tener una pantalla de la mente "
            "llena de fotos y películas. Esto te permite ser como un maestro en integrar ideas, "
            "ser creativo e innovador. Sin embargo, puedes aburrirte fácilmente y buscar "
            "constantemente nuevas cosas para aprender, aventuras y más información. Pueden ser "
            "un poco raras y divertidas para conocer, ya que su sistema de organización visual es "
            "bastante peculiar, apilas las cosas en casa: ropa, papeles,.. o en el trabajo. "
            "También tienen un sentido de humor un poco especial. A pesar de que les importa "
            "mucho la humanidad y su evolución, puede ser un poco difícil para estas personas "
            "relacionarse uno a uno con otros."
        ),
        "items": [
            "No me preocupan tanto los detalles, ya que a mí me gusta ver el panorama general.",
            "Me suelen llegar ideas frescas y creativas.",
            "Me dicen que soy muy espontáneo y con mucha energía.",
            "No me gusta hacer lo mismo una y otra vez, me aburro muy rápido de las tareas rutinarias.",
            "Me destaco en combinar ideas diferentes en algo nuevo y genial.",
            "Prefiero hacer varias cosas al mismo tiempo, me gusta multitarea.",
            "Creo que lo nuevo, lo innovador y la evolución son los valores importantes.",
            "Me resulta fácil encontrar la información en las pilas que ordeno en mi casa/oficina.",
            "Utilizo metáforas y analogías visuales para explicar mis pensamientos de una manera más divertida.",
            "Me emociono con las ideas raras o originales de los demás.",
            "A la hora de resolver problemas, confío en mi instinto y mi intuición.",
            "Tengo un sentido del humor un poco inusitado, lo que a veces me ha llevado a problemas.",
            "Algunas de mis mejores ideas surgen cuando no estoy enfocado en nada en particular.",
            "Me he convertido en un experto en organizar espacios y ver cómo reorganizar cualquier lugar.",
            "Tengo habilidades artísticas, ya sea dibujando, pintando o cualquier otra cosa.",
        ],
    },
    "Modo IV": {
        "ubicacion": "Frontal Izquierdo",
        "parrafo": (
            "El tipo de pensamiento del Modo IV es completamente lógico y analítico. Les sale "
            "bien resolver problemas complejos y encontrar soluciones que tengan lógica en la "
            "situación. Además, son geniales para usar tecnología y herramientas para lograr sus "
            "objetivos. Lo que les diferencia es su capacidad para definir metas claras y "
            "encontrar la vía más eficiente para alcanzarlas. Esto los lleva a ser líderes "
            "naturales, donde pueden tomar decisiones importantes y controlar la situación para "
            "lograr lo que quieren. Por eso, no es de extrañar que les gusten trabajar en cosas "
            "técnicas, mecánicas o financieras, donde pueden aplicar su pensamiento lógico y "
            "analítico."
        ),
        "items": [
            "Me encanta trabajar con cosas de tecnología y dinero.",
            "Me gusta analizar y resolver problemas de manera lógica.",
            "Soy bueno en arreglar y solventar problemas técnicos.",
            "Me apasiona estudiar ciencia, matemáticas y lógica.",
            "Me siento encajonado en debates y discusiones con amigos y familiares.",
            "Me gusta entender cómo funcionan las cosas y disfruto reparando o construyendo cosas.",
            "Prefiero tomar la decisión final antes que otro la tome.",
            "Creo que pensar es más importante que emocionarse.",
            "Me destaco en manejar dinero y uso muy bien mi tiempo.",
            "Me considero una persona que piensa de manera lógica.",
            "Me siento cómodo dándole órdenes y asignando tareas a otros.",
            "Me gusta organizar mi trabajo en puntos clave y procedimientos.",
            "Evalúo mi éxito en base a resultados tangibles y finales.",
            "Me considero un líder sólido y determinado.",
            "Enfoco más en la eficiencia y la racionalidad que en cualquier otro aspecto.",
        ],
    },
}

ORDEN_MODOS = ["Modo I", "Modo II", "Modo III", "Modo IV"]

# ----------------------------------------------------------------------
# FUNCIONES AUXILIARES
# ----------------------------------------------------------------------

PREGUNTAS_ALERTA = [
    {
        "pregunta": "¿En qué ambiente sentís que estudiás o trabajás mejor?",
        "A": "En un lugar con música, gente moviéndose o en un café con ruido ambiente.",
        "B": "En una biblioteca silenciosa o solo en mi cuarto con la puerta cerrada.",
    },
    {
        "pregunta": "Después de un evento social largo (como una fiesta o un día entero de clases con mucha gente), ¿cómo te sentís?",
        "A": "Con pilas; la interacción me \"despertó\" y me dio energía.",
        "B": "Agotado; necesito un tiempo a solas para \"recargarme\" y procesar todo.",
    },
    {
        "pregunta": "Si tuvieras que elegir una actividad para entrar en tu \"zona de flow\", ¿cuál preferirías?",
        "A": "Una competencia en equipo, un debate intenso o vender algo en un evento.",
        "B": "Investigar sobre un tema que me apasiona, escribir o realizar un proyecto de forma independiente.",
    },
    {
        "pregunta": "¿Cómo percibís los estímulos del entorno (luces, ruidos, conversaciones ajenas)?",
        "A": "A veces no me doy cuenta de lo que pasa alrededor; necesito que algo sea llamativo para que me \"despierte\".",
        "B": "Soy muy sensible; noto detalles, gestos y ruidos que otros parecen ignorar fácilmente.",
    },
    {
        "pregunta": "En un trabajo grupal, ¿cuál suele ser tu rol natural?",
        "A": "El que lidera la discusión, negocia con otros grupos y busca resultados rápidos.",
        "B": "El que profundiza en las ideas, analiza la información y prefiere entregar un trabajo bien reflexionado.",
    },
    {
        "pregunta": "¿Cómo describirías tu nivel de \"alerta\" al empezar el día?",
        "A": "Me cuesta arrancar; siento que mi cerebro está \"dormido\" y necesito café o música para activarme.",
        "B": "Me siento \"muy despierto\" desde temprano; los estímulos del mundo me llegan con mucha claridad enseguida.",
    },
]


def interpretar_alerta(cant_a: int, cant_b: int) -> str:
    if cant_a > cant_b:
        return ("Extravertido (Bajo nivel de alerta interior). Tu cerebro tiene un nivel de "
                "alerta natural bajo y necesita estímulos externos (\"alto volumen\") para "
                "alcanzar su punto óptimo de funcionamiento. Encontrás tu flow en ambientes "
                "dinámicos, competitivos y sociales.")
    elif cant_b > cant_a:
        return ("Introvertido (Alto nivel de alerta interior). Tu cerebro ya está en un estado "
                "de alta alerta y percibís los estímulos de forma más intensa que los demás. "
                "Encontrás tu flow en entornos de \"bajo volumen\", donde podés concentrarte sin "
                "distracciones externas.")
    else:
        return ("Equilibrado. Te sentís cómodo en entornos de \"volumen moderado\", como oficinas "
                "estándar, donde hay interacción pero también momentos de trabajo individual.")



    """Puntaje = (Parte A + cantidad de items marcados) * 5"""
    return (parte_a + items_marcados) * 5


TEXTO_EXPLICACION = """
Para entender cómo funciona tu cerebro según el modelo BTSA, imagina que tienes una
"configuración de fábrica" que determina qué tareas te resultan naturales y cuáles te agotan.
Aquí te explico las diferencias clave:

**1. Modo Dominante: Tu "Zona de Flow"**

El modo dominante es tu preferencia natural o talento innato. Es el cuadrante donde tu cerebro
gasta la mínima cantidad de energía para funcionar.

- *Cómo se siente:* Cuando lo usas, entras en un estado de "flujo" (o flow): te concentras
profundamente, te sientes feliz, el tiempo se pasa volando y actúas sin esfuerzo.
- *En la práctica:* Es aquello en lo que eres "naturalmente bueno", ya sea resolver problemas
lógicos, organizar cosas, crear ideas locas o conectar con las personas.

**2. Modos Auxiliares: Tus herramientas de apoyo**

Cada persona tiene dos modos auxiliares que son los cuadrantes vecinos a su dominante.

- *Función:* No son tu fuerte principal, pero sirven como competencias de apoyo que puedes
desarrollar y usar con relativa facilidad para completar tus tareas diarias.
- *En la práctica:* Si tu fuerte es ser creativo (Frontal Derecho), tus auxiliares podrían ser
la lógica (Frontal Izquierdo) o la empatía (Basal Derecho) para ayudarte a aterrizar tus ideas.

**3. Modo Débil: Tu "Kriptonita" energética**

El modo débil es el cuadrante que se encuentra en la diagonal opuesta a tu dominante y es el que
más energía consume.

- *Cómo se siente:* Usarlo por mucho tiempo te genera una fatiga extrema, irritabilidad y
frustración. Es esa actividad que, aunque te esfuerces, te deja "quemado" y sin ganas de nada.
- *El riesgo:* Si te obligas a vivir siempre en este modo (por exigencias de la universidad o el
trabajo), puedes sufrir lo que se llama "Desviación del Tipo", que causa estrés crónico,
agotamiento e incluso depresión.

**Dato clave para tu edad:** Entender esto ahora te ayuda a elegir una carrera o proyectos donde
puedas usar tu dominancia natural, permitiéndote ser más exitoso con mucho menos estrés.
"""


def calcular_puntaje(parte_a: int, items_marcados: int) -> int:
    """Puntaje = (Parte A + cantidad de items marcados) * 5"""
    return (parte_a + items_marcados) * 5


def interpretar(puntaje: int) -> str:
    if puntaje >= 100:
        return "Compromiso en ese Modo (Puntaje Muy Alto)"
    elif puntaje >= 65:
        return "Preferencia en ese Modo (Puntaje Alto)"
    elif puntaje >= 30:
        return "Competencia no preferida (Modo Auxiliar)"
    else:
        return "Evita ese Modo"


def clasificar_estilos(puntajes: dict) -> dict:
    """
    Devuelve un diccionario con la clasificación de cada modo:
    - 'Comprometido' : el de mayor puntaje
    - 'Preferido'    : el segundo mayor puntaje
    - 'Auxiliar'     : puntajes entre 30 y 60 (no preferidos pero presentes)
    - 'Evitado'      : puntajes entre 0 y 25
    En caso de empates, ambos modos pueden recibir la misma clasificación.
    """
    ordenado = sorted(puntajes.items(), key=lambda x: x[1], reverse=True)

    resultado = {}
    max_val = ordenado[0][1]
    second_val = ordenado[1][1] if len(ordenado) > 1 else None

    for modo, val in puntajes.items():
        if val == max_val:
            resultado[modo] = "Comprometido (Estilo dominante)"
        elif second_val is not None and val == second_val:
            resultado[modo] = "Preferido"
        elif 30 <= val <= 60:
            resultado[modo] = "Auxiliar (no preferido)"
        elif val <= 25:
            resultado[modo] = "Evitado"
        else:
            resultado[modo] = "—"

    return resultado


def grafico_plantilla(puntajes: dict):
    """
    Recrea la plantilla original de 4 cuadrantes (BTSA) y ubica un punto
    sobre la diagonal de cada cuadrante según el puntaje (0-100).
    Modo IV -> 135° (sup. izq.), Modo III -> 45° (sup. der.),
    Modo I  -> 225° (inf. izq.), Modo II -> 315° (inf. der.)
    """
    angulos = {
        "Modo IV": 135,
        "Modo III": 45,
        "Modo I": 225,
        "Modo II": 315,
    }

    etiquetas_cuadrante = {
        "Modo IV": "Lógico · Estructural · Analítico<br>Toma de decisiones complejas<br>Costo-Beneficio",
        "Modo III": "Imaginativo · Creativo · Innovador<br>Atrevido · Holístico · Artista<br>Conceptual",
        "Modo I": "Detallista · Controlador<br>Conservador · Productivo<br>Procedimientos · Calidad",
        "Modo II": "Interpersonal · Emocional<br>Espiritual · Motivador<br>Expresivo · Integrador",
    }

    pos_etiqueta = {
        "Modo IV": (-100, 100),
        "Modo III": (100, 100),
        "Modo I": (-100, -100),
        "Modo II": (100, -100),
    }

    fig = go.Figure()

    # Arcos de los cuatro cuadrantes (cuartos de círculo) + diagonales guía
    for modo, ang in angulos.items():
        start = ang - 45
        end = ang + 45
        thetas = np.linspace(np.radians(start), np.radians(end), 30)
        xs = 100 * np.cos(thetas)
        ys = 100 * np.sin(thetas)
        # arco
        fig.add_trace(go.Scatter(
            x=np.concatenate([[0], xs, [0]]),
            y=np.concatenate([[0], ys, [0]]),
            mode="lines",
            line=dict(color="lightgray", width=1),
            showlegend=False,
            hoverinfo="skip",
        ))
        # diagonal guía
        rad = np.radians(ang)
        fig.add_trace(go.Scatter(
            x=[0, 100 * np.cos(rad)],
            y=[0, 100 * np.sin(rad)],
            mode="lines",
            line=dict(color="lightgray", width=1, dash="dot"),
            showlegend=False,
            hoverinfo="skip",
        ))

    # Puntos del perfil sobre cada diagonal
    pts_x, pts_y, pts_text = [], [], []
    for modo, ang in angulos.items():
        rad = np.radians(ang)
        r = puntajes[modo]
        pts_x.append(r * np.cos(rad))
        pts_y.append(r * np.sin(rad))
        pts_text.append(f"{modo}: {r}")

    # Cerrar el polígono (orden: IV -> III -> II -> I -> IV)
    orden = ["Modo IV", "Modo III", "Modo II", "Modo I"]
    poly_x = [puntajes[m] * np.cos(np.radians(angulos[m])) for m in orden] + \
             [puntajes[orden[0]] * np.cos(np.radians(angulos[orden[0]]))]
    poly_y = [puntajes[m] * np.sin(np.radians(angulos[m])) for m in orden] + \
             [puntajes[orden[0]] * np.sin(np.radians(angulos[orden[0]]))]

    fig.add_trace(go.Scatter(
        x=poly_x, y=poly_y,
        mode="lines+markers",
        fill="toself",
        fillcolor="rgba(37, 99, 235, 0.25)",
        line=dict(color="#2563eb", width=2),
        marker=dict(size=8, color="#2563eb"),
        text=[f"{m}: {puntajes[m]}" for m in orden] + [f"{orden[0]}: {puntajes[orden[0]]}"],
        hoverinfo="text",
        showlegend=False,
    ))

    # Etiquetas de cada cuadrante
    for modo, (lx, ly) in pos_etiqueta.items():
        fig.add_annotation(
            x=lx, y=ly, text=etiquetas_cuadrante[modo],
            showarrow=False, font=dict(size=10, color="gray"),
            xanchor="center", yanchor="middle",
        )
        fig.add_annotation(
            x=0, y=0, text="", showarrow=False
        )

    # Marcas de escala 0/100
    for modo, ang in angulos.items():
        rad = np.radians(ang)
        fig.add_annotation(
            x=100 * np.cos(rad), y=100 * np.sin(rad),
            text="100", showarrow=False, font=dict(size=9, color="black"),
            xanchor="center", yanchor="middle",
        )

    fig.update_layout(
        xaxis=dict(range=[-130, 130], visible=False),
        yaxis=dict(range=[-130, 130], visible=False, scaleanchor="x", scaleratio=1),
        margin=dict(l=10, r=10, t=10, b=10),
        height=500,
        plot_bgcolor="white",
    )

    return fig


def _md_a_html(texto: str) -> str:
    """Conversión muy simple de markdown (negrita/itálica) a tags soportados por reportlab."""
    texto = texto.replace("**", "<b>", 1)
    while "**" in texto:
        texto = texto.replace("**", "</b>", 1)
        if "**" in texto:
            texto = texto.replace("**", "<b>", 1)
    texto = texto.replace("*", "<i>", 1)
    while "*" in texto:
        texto = texto.replace("*", "</i>", 1)
        if "*" in texto:
            texto = texto.replace("*", "<i>", 1)
    return texto


def generar_pdf(nombre, apellido, edad, tabla_df, comprometidos, preferidos,
                auxiliares, evitados, cant_a, cant_b, texto_alerta, fig_bytes=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm,
        leftMargin=2 * cm, rightMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Justificado", parent=styles["Normal"], alignment=TA_JUSTIFY, spaceAfter=8))
    styles.add(ParagraphStyle(name="TituloApp", parent=styles["Title"]))

    story = []

    story.append(Paragraph("Cuestionario BTSA - Resultado de Estilos de Pensamiento", styles["TituloApp"]))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph(f"Nombre: {nombre}  |  Apellido: {apellido}  |  Edad: {edad}", styles["Normal"]))
    story.append(Spacer(1, 0.5 * cm))

    # Tabla de resultados
    data = [list(tabla_df.columns)] + tabla_df.values.tolist()
    tabla = Table(data, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), "#2563eb"),
        ("TEXTCOLOR", (0, 0), (-1, 0), "white"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("GRID", (0, 0), (-1, -1), 0.5, "grey"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), ["white", "#f0f4ff"]),
    ]))
    story.append(tabla)
    story.append(Spacer(1, 0.5 * cm))

    # Gráfico de la plantilla
    if fig_bytes:
        story.append(RLImage(io.BytesIO(fig_bytes), width=14 * cm, height=14 * cm))
        story.append(Spacer(1, 0.5 * cm))

    # Resumen del perfil
    story.append(Paragraph("<b>Resumen del perfil</b>", styles["Heading2"]))
    if comprometidos:
        story.append(Paragraph(f"<b>Estilo(s) comprometido(s):</b> {', '.join(comprometidos)}", styles["Justificado"]))
    if preferidos:
        story.append(Paragraph(f"<b>Estilo(s) preferido(s):</b> {', '.join(preferidos)}", styles["Justificado"]))
    if auxiliares:
        story.append(Paragraph(f"<b>Estilo(s) auxiliar(es):</b> {', '.join(auxiliares)}", styles["Justificado"]))
    if evitados:
        story.append(Paragraph(f"<b>Estilo(s) evitado(s):</b> {', '.join(evitados)}", styles["Justificado"]))

    story.append(Spacer(1, 0.3 * cm))

    # Alerta interior
    story.append(Paragraph("<b>Alerta Interior</b>", styles["Heading2"]))
    story.append(Paragraph(f"Respuestas A: {cant_a}  |  Respuestas B: {cant_b}", styles["Normal"]))
    story.append(Paragraph(_md_a_html(texto_alerta), styles["Justificado"]))

    story.append(Spacer(1, 0.3 * cm))

    # Explicación de los estilos
    story.append(Paragraph("<b>¿Qué significan los estilos de pensamiento?</b>", styles["Heading2"]))
    for parrafo in TEXTO_EXPLICACION.strip().split("\n\n"):
        parrafo = parrafo.strip().replace("\n", " ")
        if not parrafo:
            continue
        if parrafo.startswith("- "):
            for linea in parrafo.split("\n- "):
                linea = linea.lstrip("- ")
                story.append(Paragraph("• " + _md_a_html(linea), styles["Justificado"]))
        else:
            story.append(Paragraph(_md_a_html(parrafo), styles["Justificado"]))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# ----------------------------------------------------------------------
# INTERFAZ
# ----------------------------------------------------------------------

st.title("🧠 Cuestionario BTSA")
st.caption("Determinación del estilo de pensamiento (jóvenes 17-20 años)")

with st.expander("ℹ️ ¿Cómo funciona este cuestionario?", expanded=False):
    st.markdown(
        """
        Este cuestionario evalúa **4 estilos de pensamiento** (Modo I a IV), basados en el
        modelo de cuadrantes cerebrales (BTSA / Herrmann).

        Para cada modo:
        1. Lee el párrafo descriptivo y calificá del 0 al 5 cuánto te identifica (**Parte A**).
        2. Marcá las frases que te describen mucho (dejá sin marcar las que no aplican o aplican poco).

        El **estilo de mayor puntaje** es tu estilo **comprometido**.
        El **segundo mayor puntaje** es tu estilo **preferido**.
        Los puntajes entre 30 y 60 indican **competencias no preferidas** (modo auxiliar),
        y los puntajes de 0 a 25 indican que **evitás** ese modo.
        """
    )

st.divider()

# --- Datos personales ---
st.subheader("Datos personales")
col1, col2, col3 = st.columns(3)
with col1:
    nombre = st.text_input("Nombre")
with col2:
    apellido = st.text_input("Apellido")
with col3:
    edad = st.number_input("Edad", min_value=17, max_value=20, step=1, value=17)

st.divider()

# --- Cuestionario ---
respuestas = {}

for modo, datos in MODOS.items():
    st.subheader(f"{modo}")
    st.write(datos["parrafo"])

    parte_a = st.slider(
        f"¿Cuán cómodo te sentís con este párrafo como descripción de tu persona? ({modo} - Parte A)",
        min_value=0, max_value=5, value=0, step=1,
        key=f"parteA_{modo}"
    )

    st.markdown("**Marcá las frases que te describen mucho:**")
    marcados = 0
    for i, frase in enumerate(datos["items"], start=1):
        check = st.checkbox(f"{i}. {frase}", key=f"{modo}_item_{i}")
        if check:
            marcados += 1

    respuestas[modo] = {
        "parte_a": parte_a,
        "marcados": marcados,
    }

    st.divider()

# --- Alerta Interior ---
st.subheader("Cuestionario de Alerta Interior (BTSA)")
st.write("Para cada pregunta, elegí la opción (A o B) que más te representa.")

respuestas_alerta = []
for i, p in enumerate(PREGUNTAS_ALERTA, start=1):
    st.markdown(f"**{i}. {p['pregunta']}**")
    opcion = st.radio(
        label="Elegí una opción",
        options=["A", "B"],
        format_func=lambda x, p=p: f"{x}. {p[x]}",
        key=f"alerta_{i}",
        label_visibility="collapsed",
    )
    respuestas_alerta.append(opcion)
    st.write("")

st.divider()


# ----------------------------------------------------------------------
# CÁLCULO Y RESULTADOS
# ----------------------------------------------------------------------

if st.button("🔍 Calcular resultado", type="primary", use_container_width=True):

    puntajes = {}
    for modo, datos_resp in respuestas.items():
        puntaje = calcular_puntaje(datos_resp["parte_a"], datos_resp["marcados"])
        puntajes[modo] = puntaje

    clasificacion = clasificar_estilos(puntajes)

    st.success("✅ ¡Resultado calculado!")

    if nombre or apellido:
        st.subheader(f"Resultado de {nombre} {apellido}".strip())

    # --- Tabla resumen ---
    tabla = pd.DataFrame({
        "Modo": list(puntajes.keys()),
        "Ubicación cerebral": [MODOS[m]["ubicacion"] for m in puntajes.keys()],
        "Puntaje": list(puntajes.values()),
        "Interpretación general": [interpretar(p) for p in puntajes.values()],
        "Clasificación en este perfil": [clasificacion[m] for m in puntajes.keys()],
    })

    st.dataframe(tabla, hide_index=True, use_container_width=True)

    # --- Gráfico radar ---
    st.plotly_chart(grafico_plantilla(puntajes), use_container_width=True)

    # --- Resumen narrativo ---
    st.subheader("📋 Resumen del perfil")

    comprometidos = [m for m, c in clasificacion.items() if c == "Comprometido (Estilo dominante)"]
    preferidos = [m for m, c in clasificacion.items() if c == "Preferido"]
    auxiliares = [m for m, c in clasificacion.items() if c == "Auxiliar (no preferido)"]
    evitados = [m for m, c in clasificacion.items() if c == "Evitado"]

    if comprometidos:
        st.markdown(f"**Estilo(s) comprometido(s) (de mayor puntaje):** {', '.join(comprometidos)}")
    if preferidos:
        st.markdown(f"**Estilo(s) preferido(s) (segundo mayor puntaje):** {', '.join(preferidos)}")
    if auxiliares:
        st.markdown(f"**Estilo(s) auxiliar(es) (competencias no preferidas):** {', '.join(auxiliares)}")
    if evitados:
        st.markdown(f"**Estilo(s) evitado(s):** {', '.join(evitados)}")

    st.caption(
        "Nota: el estilo comprometido y el preferido pueden coincidir con uno, dos, "
        "tres o los cuatro modos, dependiendo de los puntajes obtenidos."
    )

    st.divider()

    # --- Resultado de Alerta Interior ---
    st.subheader("🔋 Alerta Interior")

    cant_a = respuestas_alerta.count("A")
    cant_b = respuestas_alerta.count("B")

    col_a, col_b = st.columns(2)
    col_a.metric("Respuestas A", cant_a)
    col_b.metric("Respuestas B", cant_b)

    st.markdown(f"**Resultado:** {interpretar_alerta(cant_a, cant_b)}")

    st.divider()

    # --- Explicación de los estilos de pensamiento ---
    st.subheader("📖 ¿Qué significan los estilos de pensamiento?")
    st.markdown(TEXTO_EXPLICACION)

    st.divider()

    # --- Descargar PDF ---
    try:
        fig_bytes = grafico_plantilla(puntajes).to_image(format="png", width=600, height=600, scale=2)
    except Exception:
        fig_bytes = None

    pdf_bytes = generar_pdf(
        nombre, apellido, edad, tabla,
        comprometidos, preferidos, auxiliares, evitados,
        cant_a, cant_b, interpretar_alerta(cant_a, cant_b),
        fig_bytes,
    )

    st.download_button(
        label="📄 Descargar resultado en PDF",
        data=pdf_bytes,
        file_name=f"BTSA_{apellido}_{nombre}.pdf".replace(" ", "_"),
        mime="application/pdf",
        use_container_width=True,
    )



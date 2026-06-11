# Manual de uso – Cuestionario BTSA (Estilos de Pensamiento)

## 1. ¿Qué es esta app?

Es una aplicación web (hecha con Streamlit) que permite a un joven de 17 a 20 años completar
el **Cuestionario BTSA** y obtener automáticamente:

- El puntaje de cada uno de los 4 **Modos de pensamiento** (I, II, III y IV).
- Su clasificación: **Comprometido**, **Preferido**, **Auxiliar** o **Evitado**.
- Un gráfico tipo "plantilla de 4 cuadrantes" con su perfil.
- El resultado del **Cuestionario de Alerta Interior** (Extravertido / Introvertido / Equilibrado).
- Una explicación de qué significa cada tipo de modo (Dominante, Auxiliar, Débil).
- Un **PDF descargable** con todo el resultado.

---

## 2. Requisitos para correrla

La app necesita Python 3.10+ y las siguientes librerías:

```
pip install streamlit pandas plotly numpy reportlab kaleido
```

> `kaleido` es necesaria para que el gráfico se incluya como imagen dentro del PDF.
> Si no se instala, el PDF se genera igual pero sin el gráfico.

---

## 3. Cómo correrla en forma local

1. Abrir la consola (CMD) en la carpeta donde está `BTSA_App.py`.
2. Ejecutar:
   ```
   streamlit run BTSA_App.py
   ```
3. Se abre automáticamente el navegador en `http://localhost:8501`.

---

## 4. Cómo usarla (paso a paso para el joven)

1. **Datos personales**: completar Nombre, Apellido y Edad.
2. **Modos I a IV**: para cada modo:
   - Leer el párrafo descriptivo.
   - Marcar con el control deslizante (0 a 5) cuán identificado/a se siente con ese párrafo.
   - Tildar las frases (de las 15) que lo/la describen mucho. Dejar sin marcar las que no
     aplican o aplican poco.
3. **Alerta Interior**: responder las 6 preguntas eligiendo la opción A o B que más se
   identifique.
4. Hacer clic en **"🔍 Calcular resultado"**.
5. Revisar:
   - La tabla con los puntajes y la interpretación de cada modo.
   - El gráfico de 4 cuadrantes con el perfil.
   - El resumen (estilo comprometido, preferido, auxiliares, evitados).
   - El resultado de Alerta Interior.
   - La explicación de qué significa cada tipo de modo.
6. Hacer clic en **"📄 Descargar resultado en PDF"** para guardar o imprimir el informe
   completo.

---

## 5. Cómo se calcula el puntaje (referencia técnica)

Para cada Modo:

```
Puntaje = (Parte A + cantidad de frases marcadas) x 5
```

Interpretación general del puntaje:

| Rango     | Significado                                  |
|-----------|-----------------------------------------------|
| 100       | Compromiso en ese Modo (Puntaje Muy Alto)     |
| 65 - 95   | Preferencia en ese Modo (Puntaje Alto)        |
| 30 - 60   | Competencia no preferida (Modo Auxiliar)      |
| 0 - 25    | Evita ese Modo                                |

Clasificación dentro del perfil de la persona:

- **Comprometido**: el/los modo/s con el puntaje más alto.
- **Preferido**: el/los modo/s con el segundo puntaje más alto.
- **Auxiliar**: modos con puntaje entre 30 y 60 (que no sean el comprometido/preferido).
- **Evitado**: modos con puntaje entre 0 y 25.

Para Alerta Interior se cuenta cuántas respuestas A y B dio la persona:

- Mayoría de A → Extravertido (bajo nivel de alerta interior).
- Mayoría de B → Introvertido (alto nivel de alerta interior).
- Empate → Equilibrado.

---

## 6. Privacidad

La app **no guarda ni envía datos a ningún servidor**: todo el procesamiento ocurre en la
sesión del navegador del usuario, y el PDF se genera y descarga localmente. Si se publica
en Streamlit Cloud, los datos no quedan almacenados entre sesiones (a menos que se agregue
explícitamente una base de datos).

---

## 7. Soporte

Cualquier ajuste al cuestionario (textos, ítems, fórmulas de cálculo, diseño) se realiza
modificando el archivo `BTSA_App.py`. Las secciones más relevantes son:

- `MODOS`: textos y frases de cada modo.
- `PREGUNTAS_ALERTA`: preguntas del cuestionario de Alerta Interior.
- `TEXTO_EXPLICACION`: texto final sobre los estilos de pensamiento.
- `calcular_puntaje`, `interpretar`, `clasificar_estilos`: lógica de cálculo.
- `grafico_plantilla`: gráfico de 4 cuadrantes.
- `generar_pdf`: armado del informe en PDF.

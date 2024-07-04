import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Configuración de autenticación
def check_password():
    def password_entered():
        if st.session_state["password"] == "abc123":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # remove password from session state
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input("Contraseña", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Contraseña", type="password", on_change=password_entered, key="password")
        st.error("Contraseña incorrecta")
        return False
    else:
        # Password correct.
        return True

if check_password():
    # Cargar los datos
    file_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSsWwijevrZrAYC2hEP937uOTThM9gnMsIwAiNQcLffvqsapWgvULO8NnDcmWHcd2toUPRvqQYdrQwh/pub?output=csv'
    data = pd.read_csv(file_path)

    # Limpiar los datos
    data['Edad'] = data['Edad'].str.replace(' años', '', regex=False).apply(pd.to_numeric, errors='coerce')
    data['Provincia / Localidad'] = data['Provincia / Localidad'].str.strip()

    # Título de la aplicación
    st.title('Análisis de Datos de Inscripción')

    # Menú de navegación
    st.sidebar.header('Menú de Navegación')
    opciones = ['Datos Generales'] + list(data['Indicar en esta sección el/los curso/s que desea inscribirse 📝'].unique())
    seleccion = st.sidebar.selectbox('Seleccione una opción', opciones)

    if seleccion == 'Datos Generales':
        # Mostrar los datos generales
        st.header('Datos Generales')

        # Distribución de Edades
        st.subheader('Distribución de Edades')
        fig, ax = plt.subplots()
        ax.hist(data['Edad'].dropna(), bins=20, edgecolor='k')
        ax.set_xlabel('Edad')
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)

        # Nube de Palabras: Provincia / Localidad
        st.subheader('Nube de Palabras: Provincia / Localidad')
        text = ' '.join(data['Provincia / Localidad'])
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

        # Vínculo con la CTA
        st.subheader('Vínculo con la CTA')
        cta_counts = data['¿Tenes algún vínculo con la CTA?'].value_counts()
        fig, ax = plt.subplots()
        cta_counts.plot(kind='bar', ax=ax)
        ax.set_xlabel('Vínculo con la CTA')
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)

        # Medio de Conocimiento de los Cursos
        st.subheader('Medio de Conocimiento de los Cursos')
        medio_counts = data['¿Cómo te enteraste de nuestros cursos?'].value_counts()
        fig, ax = plt.subplots()
        medio_counts.plot(kind='bar', ax=ax)
        ax.set_xlabel('Medio')
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)

    else:
        # Mostrar los datos por curso
        curso_seleccionado = seleccion
        st.header(f'Datos del Curso: {curso_seleccionado}')
        data_curso = data[data['Indicar en esta sección el/los curso/s que desea inscribirse 📝'] == curso_seleccionado]

        # Distribución de Edades
        st.subheader('Distribución de Edades')
        fig, ax = plt.subplots()
        ax.hist(data_curso['Edad'].dropna(), bins=20, edgecolor='k')
        ax.set_xlabel('Edad')
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)

        # Nube de Palabras: Provincia / Localidad
        st.subheader('Nube de Palabras: Provincia / Localidad')
        text = ' '.join(data_curso['Provincia / Localidad'])
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

        # Vínculo con la CTA
        st.subheader('Vínculo con la CTA')
        cta_counts = data_curso['¿Tenes algún vínculo con la CTA?'].value_counts()
        fig, ax = plt.subplots()
        cta_counts.plot(kind='bar', ax=ax)
        ax.set_xlabel('Vínculo con la CTA')
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)

        # Medio de Conocimiento de los Cursos
        st.subheader('Medio de Conocimiento de los Cursos')
        medio_counts = data_curso['¿Cómo te enteraste de nuestros cursos?'].value_counts()
        fig, ax = plt.subplots()
        medio_counts.plot(kind='bar', ax=ax)
        ax.set_xlabel('Medio')
        ax.set_ylabel('Frecuencia')
        st.pyplot(fig)

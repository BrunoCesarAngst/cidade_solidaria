import streamlit as st
import pandas as pd
import pydeck as pdk
from opencage.geocoder import OpenCageGeocode

# Substitua 'YOUR_API_KEY' pela sua chave de API do OpenCage
API_KEY = 'YOUR_API_KEY'
geocoder = OpenCageGeocode(API_KEY)


# Função de login
def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Usuário")
    password = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Entrar"):
        if username == "admin" and password == "admin":
            st.session_state['logged_in'] = True
        else:
            st.sidebar.error("Usuário ou senha incorretos")


# Verifica se o usuário está logado
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login()
else:
    st.sidebar.success("Logado como admin")

    # Mapa interativo
    st.title("Mapa de Problemas e Ações Sociais")

    # Dados de exemplo
    if 'data' not in st.session_state:
        st.session_state['data'] = pd.DataFrame({
            'lat': [-30.0277, -30.0377],
            'lon': [-51.2287, -51.2387],
            'name': ['Problema 1', 'Problema 2']
        })

    st.map(st.session_state['data'])

    # Cadastro de problemas
    st.title("Cadastro de Problemas")
    with st.form(key='problem_form'):
        problem_name = st.text_input("Nome do Problema")
        problem_description = st.text_area("Descrição do Problema")
        problem_address = st.text_input("Endereço (Rua e Número)")
        submit_button = st.form_submit_button(label='Cadastrar Problema')

        if submit_button:
            if problem_address:
                result = geocoder.geocode(problem_address)
                if result:
                    problem_lat = result[0]['geometry']['lat']
                    problem_lon = result[0]['geometry']['lng']

                    new_data = pd.DataFrame({
                        'lat': [problem_lat],
                        'lon': [problem_lon],
                        'name': [problem_name]
                    })

                    st.session_state['data'] = pd.concat([st.session_state['data'], new_data], ignore_index=True)
                    st.success("Problema cadastrado com sucesso!")
                else:
                    st.error("Endereço não encontrado. Tente novamente.")
            else:
                st.error("Por favor, insira um endereço válido.")

            # Atualiza o mapa
            st.map(st.session_state['data'])

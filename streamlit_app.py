import streamlit as st
import pandas as pd
import pydeck as pdk
from sqlalchemy.orm import Session
from opencage.geocoder import OpenCageGeocode
import database as db_model
from database import get_db, create_user, get_user, create_problem, get_problems

# Substitua 'YOUR_API_KEY' pela sua chave de API do OpenCage
API_KEY = '7f38892f029d43b7b4b8a2979645ba37'
geocoder = OpenCageGeocode(API_KEY)


# Função de login
def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Usuário")
    password = st.sidebar.text_input("Senha", type="password")
    if st.sidebar.button("Entrar"):
        with Session(db_model.engine) as session:
            user = get_user(session, username)
            if user and user.password == password:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['user_id'] = user.id
            else:
                st.sidebar.error("Usuário ou senha incorretos")


# Função de login
def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Usuário", key="login_username")
    password = st.sidebar.text_input("Senha", type="password", key="login_password")
    if st.sidebar.button("Entrar", key="login_button"):
        with Session(db_model.engine) as session:
            user = get_user(session, username)
            if user and user.password == password:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['user_id'] = user.id
            else:
                st.sidebar.error("Usuário ou senha incorretos")

# Função de registro
def register():
    st.sidebar.title("Registrar")
    username = st.sidebar.text_input("Novo Usuário", key="register_username")
    password = st.sidebar.text_input("Senha", type="password", key="register_password")
    if st.sidebar.button("Registrar", key="register_button"):
        with Session(db_model.engine) as session:
            if get_user(session, username):
                st.sidebar.error("Usuário já existe")
            else:
                create_user(session, username, password)
                st.sidebar.success("Registrado com sucesso. Faça login.")

# Verifica se o usuário está logado
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login()
    register()
else:
    st.sidebar.success(f"Logado como {st.session_state['username']}")

    # Mapa interativo
    st.title("Mapa de Problemas e Ações Sociais")

    with Session(db_model.engine) as session:
        problems = get_problems(session, st.session_state['user_id'])
        df = pd.DataFrame([(p.name, p.description, p.latitude, p.longitude) for p in problems],
                          columns=['name', 'description', 'lat', 'lon'])

    if not df.empty:
        st.map(df)

    # Cadastro de problemas
    st.title("Cadastro de Problemas")
    with st.form(key='problem_form'):
        problem_name = st.text_input("Nome do Problema", key="problem_name")
        problem_description = st.text_area("Descrição do Problema", key="problem_description")
        problem_address = st.text_input("Endereço (Rua e Número)", key="problem_address")
        submit_button = st.form_submit_button(label='Cadastrar Problema')

        if submit_button:
            if problem_address:
                result = geocoder.geocode(problem_address)
                if result:
                    problem_lat = result[0]['geometry']['lat']
                    problem_lon = result[0]['geometry']['lng']

                    with Session(db_model.engine) as session:
                        create_problem(session, problem_name, problem_description, problem_lat, problem_lon, st.session_state['user_id'])
                    st.success("Problema cadastrado com sucesso!")

                    # Atualizar os dados e o mapa
                    with Session(db_model.engine) as session:
                        problems = get_problems(session, st.session_state['user_id'])
                        df = pd.DataFrame([(p.name, p.description, p.latitude, p.longitude) for p in problems],
                                          columns=['name', 'description', 'lat', 'lon'])
                    st.map(df)
                else:
                    st.error("Endereço não encontrado. Tente novamente.")
            else:
                st.error("Por favor, insira um endereço válido.")

    # Listar problemas cadastrados
    st.title("Problemas Cadastrados")
    if not df.empty:
        st.dataframe(df)

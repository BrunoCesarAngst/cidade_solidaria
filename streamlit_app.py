import pandas as pd
import streamlit_authenticator as stauth
import streamlit as st
from sqlalchemy.orm import Session
from streamlit_authenticator.utilities.hasher import Hasher
from validate_docbr import CPF
import database as db_model
from database import create_user, get_user, create_problem, get_all_problems, get_all_users
from init_cidade_solidaria import initialize
from map_cidade_solidaria import show_map
from register_user import register_user

db_url, geocoder = initialize()

# def create_problem_form():
#     st.title("Cadastrar marcação")
#     with st.form(key='problem_form'):
#         title = st.text_input("Título", max_chars=40, key="problem_title")
#         tags = st.text_input("Tags", max_chars=255, key="problem_tags")
#         description = st.text_area("Descrição", key="problem_description")
#         state = st.text_input("Estado", key="problem_state")
#         city = st.text_input("Cidade", key="problem_city")
#         zipcode = st.text_input("CEP", key="problem_zipcode")
#         street = st.text_input("Rua", key="problem_street")
#         number = st.text_input("Número", key="problem_number")
#         reference = st.text_input("Referência", key="problem_reference")
#         submit_button = st.form_submit_button(label='Cadastrar ponto')
#
#         if submit_button:
#             address = f"{street}, {number}, {city}, {state}, {zipcode}"
#             result = geocoder.geocode(address)
#             if result:
#                 lat = result[0]['geometry']['lat']
#                 lon = result[0]['geometry']['lng']
#                 with Session(db_model.engine) as session:
#                     create_problem(session, title, tags, description, lat, lon, state, city, zipcode, street, number, reference, st.session_state['user_id'])
#                 st.success("Problema cadastrado com sucesso!")
#             else:
#                 st.error("Endereço não encontrado. Tente novamente.")

def show_partners():
    st.title("Parceiros")
    st.write("Aqui estão os parceiros do app...")

def show_support():
    st.title("Apoie o App")
    st.write("Aqui estão as formas de apoiar o app...")

def main():
    fields = {
        'username': 'Usuário',
        'password': 'Senha',
        'login': 'Entrar'
    }
    with Session(db_model.engine) as session:
        users = get_all_users(session)

    credentials ={}
    credentials['usernames'] = {}

    for user in users:
        credentials['usernames'][user.email] = {
            "email": user.email,
            "failed_login_attempts": 0,
            "logged_in": False,
            "name": user.full_name,
            "password": user.password
        }

    authenticator = stauth.Authenticate(credentials, cookie_name='cookie_cidade_solidaria', cookie_key='.',
                                        cookie_expiry_days=30)

    name, authentication_status, username = authenticator.login(fields=fields, location='main')

    if authentication_status:
        authenticator.logout("Logout", "sidebar")
        st.sidebar.success(f"Logado como {name}")

        # Inicializar user_id no session_state
        with Session(db_model.engine) as session:
            user = get_user(session, username)
            st.session_state['user_id'] = user.id if user else None

        st.session_state['logged_in'] = True
    elif authentication_status == False:
        st.error("Usuário/Senha incorretos")
        st.session_state['logged_in'] = False
    elif authentication_status == None:
        st.warning("Por favor, entre com suas credenciais")
        st.session_state['logged_in'] = False

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    menu = ["Mapa", "Parceiros", "Apoie", "Registrar", "Login"] if not st.session_state['logged_in'] else ["Mapa", "Cadastrar Problema", "Parceiros", "Apoie", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Mapa":
        st.title("Mapa de Problemas e Ações Sociais")
        show_map()
    elif choice == "Parceiros":
        show_partners()
    elif choice == "Apoie":
        show_support()
    elif choice == "Registrar":
        register_user()
    elif choice == "Login":
        pass
    elif choice == "Cadastrar Problema":
        if st.session_state['logged_in']:
            pass
            #create_problem_form()
        else:
            st.error("Por favor, faça login para cadastrar um problema.")
    elif choice == "Logout":
        st.session_state['logged_in'] = False
        st.experimental_rerun()

if __name__ == "__main__":
    main()

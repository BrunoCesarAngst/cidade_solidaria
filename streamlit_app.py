import os

import bcrypt  # Importando biblioteca para hash de senhas
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from dotenv import load_dotenv
from opencage.geocoder import OpenCageGeocode
from sqlalchemy.orm import Session
from validate_docbr import CPF
from yaml.loader import SafeLoader

import database as db_model
from database import create_user, get_user, create_problem, get_all_problems

# Carregar variáveis de ambiente
load_dotenv()
API_KEY = os.getenv("API_KEY")
ENVIRONMENT = os.getenv("ENVIRONMENT")
DATABASE_URL = os.getenv(f"DATABASE_URL_{ENVIRONMENT.upper()}")

# Inicializar geocoder
geocoder = OpenCageGeocode(API_KEY)

# Carregar o arquivo de configuração
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Configurar autenticação
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

# Funções de hash e verificação de senha
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Funções de validação
def validate_cpf(cpf):
    cpf_validator = CPF()
    return cpf_validator.validate(cpf)

def validate_password(password, confirm_password):
    return password == confirm_password

def register_user():
    st.sidebar.title("Registrar")
    full_name = st.sidebar.text_input("Nome Completo", max_chars=255, key="register_full_name")
    cpf = st.sidebar.text_input("CPF", max_chars=11, key="register_cpf")
    email = st.sidebar.text_input("Email", max_chars=255, key="register_email")
    password = st.sidebar.text_input("Senha", type="password", key="register_password")
    confirm_password = st.sidebar.text_input("Senha novamente", type="password", key="register_confirm_password")
    if st.sidebar.button("Registrar", key="register_button"):
        with Session(db_model.engine) as session:
            if validate_cpf(cpf) and validate_password(password, confirm_password):
                if not get_user(session, email):
                    hashed_password = hash_password(password)
                    create_user(session, full_name, cpf, email, hashed_password)
                    st.sidebar.success("Registrado com sucesso. Faça login.")
                else:
                    st.sidebar.error("Email já cadastrado")
            else:
                st.sidebar.error("Erro na validação de CPF ou senhas não coincidem")

def show_map():
    with Session(db_model.engine) as session:
        problems = get_all_problems(session)
        df = pd.DataFrame([(p.title, p.tags, p.description, p.latitude, p.longitude, p.state, p.city, p.zipcode, p.street, p.number, p.reference) for p in problems],
                          columns=['title', 'tags', 'description', 'lat', 'lon', 'state', 'city', 'zipcode', 'street', 'number', 'reference'])
    st.map(df)
    for _, row in df.iterrows():
        st.write(f"**{row['title']}** - {row['tags']}")
        st.write(f"{row['description']}")
        st.write(f"{row['street']}, {row['number']}, {row['city']}, {row['state']}, {row['zipcode']}")
        st.write(f"Referência: {row['reference']}")
        st.write("---")

def create_problem_form():
    st.title("Cadastro de Problemas/Ações Sociais")
    with st.form(key='problem_form'):
        title = st.text_input("Título", max_chars=40, key="problem_title")
        tags = st.text_input("Tags", max_chars=255, key="problem_tags")
        description = st.text_area("Descrição", key="problem_description")
        state = st.text_input("Estado", key="problem_state")
        city = st.text_input("Cidade", key="problem_city")
        zipcode = st.text_input("CEP", key="problem_zipcode")
        street = st.text_input("Rua", key="problem_street")
        number = st.text_input("Número", key="problem_number")
        reference = st.text_input("Referência", key="problem_reference")
        submit_button = st.form_submit_button(label='Cadastrar Problema')

        if submit_button:
            address = f"{street}, {number}, {city}, {state}, {zipcode}"
            result = geocoder.geocode(address)
            if result:
                lat = result[0]['geometry']['lat']
                lon = result[0]['geometry']['lng']
                with Session(db_model.engine) as session:
                    create_problem(session, title, tags, description, lat, lon, state, city, zipcode, street, number, reference, st.session_state['user_id'])
                st.success("Problema cadastrado com sucesso!")
            else:
                st.error("Endereço não encontrado. Tente novamente.")

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
            create_problem_form()
        else:
            st.error("Por favor, faça login para cadastrar um problema.")
    elif choice == "Logout":
        st.session_state['logged_in'] = False
        st.experimental_rerun()

if __name__ == "__main__":
    main()

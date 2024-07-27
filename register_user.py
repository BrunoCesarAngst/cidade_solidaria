
import streamlit as st
from sqlalchemy.orm import Session
from streamlit_authenticator.utilities.hasher import Hasher
from validate_docbr import CPF
import database as db_model
from database import create_user, get_user


def validate_cpf(cpf):
    cpf_validator = CPF()
    return cpf_validator.validate(cpf)

def validate_password(password, confirm_password):
    return password == confirm_password

def hash_password(password):
    return Hasher._hash(password)
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
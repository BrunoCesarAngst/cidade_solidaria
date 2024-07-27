import os
from dotenv import load_dotenv
from opencage.geocoder import OpenCageGeocode
import yaml
from yaml import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth

def load_environment():
    load_dotenv()
    environment = os.getenv("ENVIRONMENT")
    if not environment:
        raise Exception("ENVIRONMENT variável não definida ou inválida!")
    return environment


def load_secrets():
    try:
        secrets = {
            "api_key": st.secrets["general"]["api_key"],
            "db_url_local": st.secrets["database"]["url_local"],
            "db_url_docker": st.secrets["database"]["url_docker"],
            "db_url_production": st.secrets["database"]["url_production"]
        }
        return secrets
    except KeyError as e:
        raise Exception(
            f"Segredo {e} não encontrado. Verifique o arquivo secrets.toml ou as configurações de segredos no Streamlit Cloud.")


def get_db_url(environment, secrets):
    environment = environment.lower()
    if environment == "production":
        return secrets["db_url_production"]
    elif environment == "development":
        return secrets["db_url_docker"]
    else:
        return secrets["db_url_local"]


def initialize_geocoder(api_key):
    return OpenCageGeocode(api_key)




def initialize():
    environment = load_environment()
    secrets = load_secrets()
    db_url = get_db_url(environment, secrets)
    geocoder = initialize_geocoder(secrets["api_key"])
    return db_url, geocoder

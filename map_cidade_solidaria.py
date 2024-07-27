import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.elements import MacroElement
from jinja2 import Template


class LatLngPopup(MacroElement):
    """
    Quando se clica em um Mapa que contém LatLngPopup,
    um popup é mostrado exibindo a latitude e longitude do ponteiro.
    """
    _template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.popup();
                function latLngPop(e) {
                var data = e.latlng.lat.toFixed(4) + "," + e.latlng.lng.toFixed(4);
                    {{this.get_name()}}
                        .setLatLng(e.latlng)
                        .setContent("<br /><a href='/create_marker?lat=" + e.latlng.lat + "&lng=" + e.latlng.lng + "' target='_self'>Criar marcação</a>")
                        .openOn({{this._parent.get_name()}});
                }
                {{this._parent.get_name()}}.on('click', latLngPop);
            {% endmacro %}
            """)

    def __init__(self):
        super(LatLngPopup, self).__init__()
        self._name = 'LatLngPopup'

# Função para adicionar um marcador com texto acima e score em destaque
def add_marker_with_text_and_score(map_obj, location, text, url, score):
    # Adiciona o marcador
    marker = folium.Marker(
        location=location,
        icon=folium.Icon(color='blue', icon='plus', prefix='fa')
    ).add_to(map_obj)

    # HTML e CSS para o círculo de score e o texto
    html = f"""
    <div class="custom-marker" style="position: relative; bottom: 40px; left: -30px; text-align: center;">
        <div style="position: absolute; top: -10px; left: -5px; background: red; color: white; border-radius: 50%; padding: 5px 10px; font-size: 12px;">
            {score}
        </div>        
    </div>
    <a href="{url}" target="_blank" style="text-decoration: none; color: black;">
        <div style="position: absolute; top: -50px; left: 0px; background: white; color: black; border-radius: 10%; padding: 1px 1px; font-size: 12px; text-align: center;">
            {text}
        </div>
    </a>
    """
    folium.Marker(
        location,
        icon=folium.DivIcon(
            html=html
        )
    ).add_to(map_obj)

# Cria o mapa centrado em uma localização específica
def show_map():
    map_center = [-30.7749, -51.4194]
    m = folium.Map(location=map_center, zoom_start=10, min_zoom=4, max_zoom=16)

    points = [
        {"location": [-30.7749, -51.4194], "text": "Solidarismo_Irmandade_camino_da_ascensão", "url": "https://exemplo.com/ponto1", "score": 9.8},
        {"location": [-30.7849, -50.4094], "text": "Horta comunitaria", "url": "https://exemplo.com/ponto2", "score": 7.2}
    ]

    # Adiciona os pontos ao mapa com texto acima e redirecionamento
    for point in points:
        add_marker_with_text_and_score(m, point["location"], point["text"], point["url"], point["score"])

    # Adiciona o popup de lat/long ao mapa
    m.add_child(LatLngPopup())

    # Exibe o mapa usando streamlit_folium
    st_folium(m, width=700, height=500)


# Função para criar um novo marcador
def create_marker(lat, lon):
    st.title("Cadastrar Marcação")
    with st.form(key='marker_form'):
        title = st.text_input("Título", max_chars=40, key="marker_title")
        tags = st.text_input("Tags", max_chars=255, key="marker_tags")
        description = st.text_area("Descrição", key="marker_description")
        score = st.number_input("Score", min_value=1.0, max_value=10.0, step=0.1, key="marker_score")
        submit_button = st.form_submit_button(label='Cadastrar ponto')

        if submit_button:
            # Aqui você pode adicionar a lógica para salvar os dados no banco de dados
            # Por enquanto, vamos apenas adicionar o marcador ao mapa
            st.session_state.create_marker = False
            map_center = [lat, lon]
            m = folium.Map(location=map_center, zoom_start=10, min_zoom=4, max_zoom=16)
            add_marker_with_text_and_score(m, map_center, title, "#", score)
            st.success("Marcação cadastrada com sucesso!")
            st_folium(m, width=700, height=500)


show_map()

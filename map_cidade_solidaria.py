import streamlit as st
import folium
from streamlit_folium import st_folium

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

    # Adiciona o JavaScript para controlar a visibilidade dos marcadores com base no zoom
    zoom_script = """
    <script>
        function updateMarkerVisibility() {
            var zoomLevel = map.getZoom();
            var elements = document.getElementsByClassName('custom-marker');
            for (var i = 0; i < elements.length; i++) {
                if (zoomLevel > 10) {
                    elements[i].style.display = 'none';
                } else {
                    elements[i].style.display = 'block';
                }
            }
        }

        map.on('zoomend', updateMarkerVisibility);
        updateMarkerVisibility();
    </script>
    """

    # Adiciona o script ao mapa
    m.get_root().html.add_child(folium.Element(zoom_script))

    # Exibe o mapa usando streamlit_folium
    st_folium(m, width=700, height=500)


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
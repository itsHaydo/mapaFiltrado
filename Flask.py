
from flask import Flask, request
import pandas as pd
import folium
from folium.plugins import MarkerCluster

app = Flask(__name__)

@app.route('/update_map', methods=['POST'])
def update_map():
    datos = pd.read_csv('CSV/housing.csv', header=None, skiprows=1)

    selected_filter = request.form['filter']
    filtered_data = datos  # Aquí debes filtrar los datos según el filtro seleccionado

    mapa_actualizado = folium.Map(location=[filtered_data[1].mean(), filtered_data[0].mean()], zoom_start=8)
    cluster = MarkerCluster().add_to(mapa_actualizado)

    for i, (latitud, longitud, age, rooms, bedrooms, pop, households, income, value, proximity) in enumerate(
            zip(filtered_data[1], filtered_data[0], filtered_data[2], filtered_data[3], filtered_data[4],
                filtered_data[5], filtered_data[6], filtered_data[7], filtered_data[8], filtered_data[9])):

        popup = contenido(age, rooms, bedrooms, pop, households, income, value, proximity)

        folium.Marker(
            location=[latitud, longitud],
            popup=folium.Popup(popup, max_width=300),
            icon=folium.Icon(color='blue')
        ).add_to(cluster)

    return mapa_actualizado.get_root().html.render()

if __name__ == '__main__':
    app.run(debug=True)

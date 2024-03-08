
from flask import Flask, render_template, request
import pandas as pd
import folium
from folium.plugins import MarkerCluster

app = Flask(__name__)

datos = pd.read_csv('CSV/housing.csv', header=None, skiprows=1)
datos.columns = ['Longitude', 'Latitude', 'Age', 'Rooms', 'Bedrooms', 'Population', 'Households', 'Income', 'Value', 'Ocean Proximity']

def contenido(age, rooms, bedrooms, pop, households, income, value, proximity):
    texto = f'''<strong>Edad media de la vivienda:</strong> {age}<br>
                <strong>Total de habitaciones:</strong> {rooms}<br>
                <strong>Total de dormitorios:</strong> {bedrooms}<br>
                <strong>Población:</strong> {pop}<br>
                <strong>Hogares:</strong> {households}<br>
                <strong>Ingreso mediano:</strong> {income}<br>
                <strong>Valor mediano de la vivienda:</strong> {value}<br>
                <strong>Proximidad al océano:</strong> {proximity}'''

    return texto


@app.route('/')
def index():
    mapa = folium.Map(location=[datos['Latitude'].mean(), datos['Longitude'].mean()], zoom_start=5)
    cluster = MarkerCluster().add_to(mapa)

    for i, (latitud, longitud, age, rooms, bedrooms, pop, households, income, value, proximity) in enumerate(
            zip(datos['Latitude'], datos['Longitude'], datos['Age'], datos['Rooms'],
                datos['Bedrooms'], datos['Population'], datos['Households'],
                datos['Income'], datos['Value'], datos['Ocean Proximity'])):

        popup = contenido(age, rooms, bedrooms, pop, households, income, value, proximity)

        folium.Marker(
            location=[latitud, longitud],
            popup=folium.Popup(popup, max_width=300),
            icon=folium.Icon(color='blue')
        ).add_to(cluster)

    return render_template('index.html', mapa=mapa._repr_html_())


@app.route('/update_map', methods=['POST'])
def update_map():
    selected_filter = request.form['filter1']
    selected_filter2 = request.form['filter2']
    selected_filter3 = request.form['filter3']

    if selected_filter == 'all':
        filtered_data = datos
    elif selected_filter == 'inland':
        filtered_data = datos[datos['Ocean Proximity'] == 'INLAND']
    elif selected_filter == 'near_bay':
        filtered_data = datos[datos['Ocean Proximity'] == 'NEAR BAY']
    elif selected_filter == 'very_near_bay':
        filtered_data = datos[datos['Ocean Proximity'] == '<1H OCEAN']
    elif selected_filter == 'island':
        filtered_data = datos[datos['Ocean Proximity'] == 'ISLAND']
    else:
        filtered_data = datos

    # Filtrar según el segundo filtro
    if selected_filter2 == 'precio-grande':
        filtered_data = filtered_data[filtered_data['Value'] > 350000]
    elif selected_filter2 == 'precio-mediano':
        filtered_data = filtered_data[(filtered_data['Value'] >= 180000) & (filtered_data['Value'] <= 349999)]
    elif selected_filter2 == 'precio-':
        filtered_data = filtered_data[filtered_data['Value'] < 180000]

    # Filtrar según el tercer filtro
    if selected_filter3 == 'edad-grande':
        filtered_data = filtered_data[filtered_data['Age'] > 35]
    elif selected_filter3 == 'edad-mediano':
        filtered_data = filtered_data[(filtered_data['Age'] >= 18) & (filtered_data['Age'] <= 34)]
    elif selected_filter3 == 'edad-pequeña':
        filtered_data = filtered_data[filtered_data['Age'] < 18]

    mapa = folium.Map(location=[filtered_data['Latitude'].mean(), filtered_data['Longitude'].mean()], zoom_start=8)
    cluster = MarkerCluster().add_to(mapa)

    for i, (latitud, longitud, age, rooms, bedrooms, pop, households, income, value, proximity) in enumerate(
            zip(filtered_data['Latitude'], filtered_data['Longitude'], filtered_data['Age'], filtered_data['Rooms'],
                filtered_data['Bedrooms'], filtered_data['Population'], filtered_data['Households'],
                filtered_data['Income'], filtered_data['Value'], filtered_data['Ocean Proximity'])):

        popup = contenido(age, rooms, bedrooms, pop, households, income, value, proximity)

        folium.Marker(
            location=[latitud, longitud],
            popup=folium.Popup(popup, max_width=300),
            icon=folium.Icon(color='blue')
        ).add_to(cluster)

    return mapa._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)


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
    return render_template('index.html')

@app.route('/update_map', methods=['POST'])
def update_map():
    selected_age_filter = request.form.get('age_filter')
    selected_rooms_filter = request.form.get('rooms_filter')
    selected_bedrooms_filter = request.form.get('bedrooms_filter')
    selected_population_filter = request.form.get('population_filter')
    selected_households_filter = request.form.get('households_filter')
    selected_median_income_filter = request.form.get('median_income_filter')
    selected_median_house_value_filter = request.form.get('median_house_value_filter')
    selected_ocean_filter = request.form.get('ocean_filter')

    filtered_data = datos

    if selected_age_filter != 'all':
        age_range = selected_age_filter.split(' - ')
        filtered_data = filtered_data[(filtered_data['Age'] >= float(age_range[0])) & (filtered_data['Age'] <= float(age_range[1]))]

    if selected_bedrooms_filter != 'all':
        bedrooms_range = selected_bedrooms_filter.split(' - ')
        filtered_data = filtered_data[(filtered_data['Bedrooms'] >= int(bedrooms_range[0])) & (filtered_data['Bedrooms'] <= int(bedrooms_range[1]))]

    if selected_ocean_filter != 'all':
        filtered_data = filtered_data[filtered_data['Ocean Proximity'] == selected_ocean_filter]

    mapa = folium.Map(location=[filtered_data['Latitude'].mean(), filtered_data['Longitude'].mean()], zoom_start=5)
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

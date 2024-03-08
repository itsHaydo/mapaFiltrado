from flask import Flask, render_template, request
import pandas as pd
import folium
from folium.plugins import MarkerCluster

app = Flask(__name__)

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

@app.route('/update_map', methods=['POST'])
def update_map():
    datos = pd.read_csv('CSV/housing.csv', header=None, skiprows=1)

    selected_age_filter = request.form.get('age_filter')
    selected_rooms_filter = request.form.get('rooms_filter')
    selected_bedrooms_filter = request.form.get('bedrooms_filter')
    selected_population_filter = request.form.get('population_filter')
    selected_households_filter = request.form.get('households_filter')
    selected_median_income_filter = request.form.get('median_income_filter')
    selected_median_house_value_filter = request.form.get('median_house_value_filter')
    selected_filter = request.form['filte']

    filtered_data = datos

    #if selected_age_filter != 'all':
     #   age_range = selected_age_filter.split(' - ')
      #  filtered_data = filtered_data[(filtered_data['Age'] >= float(age_range[0])) & (filtered_data['Age'] <= float(age_range[1]))]

    #if selected_bedrooms_filter != 'all':
     #   bedrooms_range = selected_bedrooms_filter.split(' - ')
      #  filtered_data = filtered_data[(filtered_data['Bedrooms'] >= int(bedrooms_range[0])) & (filtered_data['Bedrooms'] <= int(bedrooms_range[1]))]

    #if selected_ocean_filter != 'all':
        #filtered_data = filtered_data[filtered_data['Ocean Proximity'] == selected_ocean_filter]

    mapa = folium.Map(location=[filtered_data[1].mean(), filtered_data[0].mean()], zoom_start=8)
    cluster = MarkerCluster().add_to(mapa)

    for i, (latitud, longitud, age, rooms, bedrooms, pop, households, income, value, proximity) in enumerate(
            zip(filtered_data[1], filtered_data[0], filtered_data[2], filtered_data[3], filtered_data[4],
                filtered_data[5], filtered_data[6], filtered_data[7], filtered_data[8], filtered_data[9])):

        popup = contenido(age, rooms, bedrooms, pop, households, income, value, proximity)

        folium.Marker(
            location=[latitud, longitud],
            popup=folium.Popup(popup, max_width=300),
            icon=folium.Icon(color='blue')
        ).add_to(cluster)

    return mapa.get_root().html.render()


if __name__ == '__main__':
    app.run(debug=True)

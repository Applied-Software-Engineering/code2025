import requests
from flask import Flask, render_template_string, render_template, request
import folium


def create_app():

    # The server url address
    # server_url = "https://bogartpamela-dramavenice-5000.codio-box.uk/"
    server_url = 'http://localhost:4500/nearest'

    bank_types = ['all', 'Packaging', 'Paper Bank', 'Bottle Bank - Mixed', 'Textile Bank',
                  'Bottle Bank - Brown', 'Bottle Bank - Clear', 'Bottle Bank - Green',
                  'Can Banks', 'Book Bank', 'Compost Bins', 'Plastic Bank']

    app = Flask(__name__)


    @app.route('/')
    def index():
        """
        Returns the index page that is a form enter a user location and type of recycling center they want to find
        :return:
        """
        return render_template('index.html', recycle_types=bank_types)

    @app.route('/test')
    def test():
        """
        Simple test example and get a json response
        :return:
        """

        my_loc = {'latitude': 55.32, 'longitude': -3.1}
        response = requests.post(server_url , json=my_loc)

        if response.status_code >= 400:
            return render_template_string(f'Request failed with status code: {response.status_code}')

        return response.json()

    @app.route('/map', methods=['POST'])
    def map():

        # Gte the form data
        location = request.form.get('location')
        no_items = int(request.form.get('no_items'))
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))
        bank_type = request.form.get('bank_type')

        # create geo location as list of the latitude and longitude
        my_geo_loc = [latitude, longitude]

        # create a query for our server
        my_query = {'latitude': latitude, 'longitude': longitude, 'no_items':no_items, 'bank_type':bank_type}

        response = requests.post(server_url , json=my_query)
        print(response.json())

        # Check we have a suitable response
        if response.status_code >= 400:
            return render_template_string(f'Request failed with status code: {response.status_code}')

        # process the response
        data = response.json()
        center_name = data['site_name']
        center_lat = data['latitude']
        center_long = data['longitude']
        center_geo_loc = [center_lat, center_long]

        # Create the Folium map object
        edinburgh_geoloc = [55.953333,-3.189167]
        map = folium.Map(location=edinburgh_geoloc, zoom_start=12)

        # add marker for my location
        my_loc_icon = folium.Icon(color='red')
        folium.Marker(location=my_geo_loc, popup=location, icon=my_loc_icon).add_to(map)

        # add marker for the nearest center
        folium.Marker(location=center_geo_loc, popup=center_name).add_to(map)

        # return html with the map
        return render_template('map.html', map=map._repr_html_())

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
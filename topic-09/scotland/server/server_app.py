import folium as folium
import haversine as haversine
from flask import Flask, render_template, jsonify, request
from os import path
import pandas as pd
from haversine import haversine, Unit


def create_app():
    app = Flask(__name__)
    recycling_data = path.join('res', 'edinburgh_council_recycling_points.csv')
    df = pd.read_csv(recycling_data)
    bank_types = ['all', 'Packaging', 'Paper Bank', 'Bottle Bank - Mixed', 'Textile Bank',
                  'Bottle Bank - Brown', 'Bottle Bank - Clear', 'Bottle Bank - Green',
                  'Can Banks', 'Book Bank', 'Compost Bins', 'Plastic Bank']
    colors = [
        '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FFA500',
        '#800080', '#FFC0CB', '#A52A2A', '#00FFFF', '#FF00FF',
        '#808080', '#008080'
    ]
    bank_color_dict = dict(zip(bank_types, colors))

    @app.route('/status')
    def status():
        print(df.head())
        return render_template("status.html")

    @app.route("/nearest", methods=['POST'])
    def get_nearest():
        if request.method != 'POST':
            error_message = {'error': 'Invalid request method. Only POST requests are allowed.'}
            return jsonify(error_message), 405
        json = request.get_json()
        print(json)
        latitude = json.get('latitude')
        longitude = json.get('longitude')

        # Check if latitude and longitude are valid numbers
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            error_message = {'error': 'Invalid latitude or longitude value.'}
            return jsonify(error_message), 400  # Return a 400 Bad Request status code

        # Perform additional validation if needed
        if latitude < -90 or latitude > 90 or longitude < -180 or longitude > 180:
            error_message = {'error': 'Latitude or longitude out of range.'}
            return jsonify(error_message), 400  # Return a 400 Bad Request status code

        geo_loc_given = [latitude, longitude]

        # Process the data as needed
        bank_type = 'all'
        if json.get('bank_type') is not None:
            bank_type = json.get('bank_type')
        print(bank_type)
        current_item = df.iloc[0]
        if bank_type == 'all':
            current_item = df.iloc[0]
            geo_loc = [float(current_item[3]), float(current_item[4])]
            current_dist = haversine(geo_loc, geo_loc_given)
            for item in df.drop_duplicates(subset=['Site_Name']).iterrows():
                geo_loc = [item[1][3], item[1][4]]
                dist = haversine(geo_loc, geo_loc_given, unit=Unit.MILES)
                if (current_dist > dist):
                    current_dist = dist
                    print(dist)
                    current_item = item[1]
        else:
            condition = df['BankTypeNa'] == bank_type
            current_item = df.loc[condition].iloc[0]
            geo_loc = [float(current_item[3]), float(current_item[4])]
            current_dist = haversine(geo_loc, geo_loc_given)
            for item in df.iterrows():
                if item[1][2] == bank_type:
                    geo_loc = [item[1][3], item[1][4]]
                    dist = haversine(geo_loc, geo_loc_given, unit=Unit.MILES)
                    if (current_dist > dist):
                        current_dist = dist
                        print(dist)
                        current_item = item[1]

        if current_item is None:
            error_message = {'None Found'}
            return jsonify(error_message), 404  # Return a 400 Bad Request status code

        site_name = current_item[0]
        site_address = current_item[1]
        latitude = current_item[3]
        longitude = current_item[4]

        json = {'latitude': latitude, 'longitude': longitude, 'site_name': site_name, 'site_address': site_address}
        return jsonify(json)

    @app.route('/map')
    def get_map():
        return get_map_with_limit(30)

    @app.route('/map/<int:limit>', methods=['GET'])
    def get_map_with_limit(limit):
        """
        Generate a map of the first 30 unique recycling centers
        :return:
        """
        edinburgh_geoloc = [55.953333, -3.189167]
        # Create a Folium map object
        map = folium.Map(location=edinburgh_geoloc, zoom_start=12)

        # Add a marker to the map
        # drop all duplicate site names, as we are interested in unique locations
        for item in df.drop_duplicates(subset=['Site_Name']).head(limit).iterrows():
            latitude = float(item[1][3])
            longitude = float(item[1][4])
            # lat, log
            geo_loc = [latitude, longitude]
            site_name = item[1]

            folium.Marker(location=geo_loc, popup=site_name).add_to(map)
        return render_template('map.html', map=map._repr_html_())


    @app.route('/map/<bank_type>')
    def get_map_type(bank_type):
        return get_map_type_with_limit(bank_type, 30)


    @app.route('/map/<bank_type>/<int:limit>', methods=['GET'])
    def get_map_type_with_limit(bank_type, limit):
        edinburgh_geoloc = [55.953333, -3.189167]
        # Create a Folium map object
        map = folium.Map(location=edinburgh_geoloc, zoom_start=12)

        # Add a marker to the map
        print(f'type = {bank_type}')
        # find all the sites that match that bank_type subject to a limit
        for item in df.loc[df['BankTypeNa'] == bank_type].head(limit).iterrows():
            latitude = float(item[1][3])
            longitude = float(item[1][4])
            # lat, log
            geo_loc = [latitude, longitude]
            site_name = item[1]
            icon_colour = folium.Icon(color=bank_color_dict[bank_type])
            folium.Marker(location=geo_loc, popup=site_name, icon=icon_colour).add_to(map)
        return render_template('map.html', map=map._repr_html_())

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=4500)

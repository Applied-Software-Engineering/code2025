import folium


# using folium

def get_full_map():
    return folium.Map().get_root().render()


def get_political():
    political_countries_url = (
        "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    )

    m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")

    m.get_root().width = "800px"
    m.get_root().height = "600px"

    folium.GeoJson(political_countries_url).add_to(m)
    return m.get_root().render()


if __name__ == "__main__":
    pass
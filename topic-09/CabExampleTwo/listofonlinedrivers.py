import gc

from flask import render_template
from flask_googlemaps import Map

from main import app, login_required


@app.route('/listofonlinedrivers')
@login_required
def listofonlinedrivers():
    try:

        c, conn = connection()
        c.execute("SELECT * from OnlineDriver")

        onlinedrivers = []
        x = c.fetchall()
        conn.commit()
        c.close()
        gc.collect()

        for row in x:
            z = {
                "username": row[0]
            }
            onlinedrivers.append(z)

        # correct upto above line. Any mistakes that will occur will be from below here

        onlinedriversinfo = []
        for a in onlinedrivers:
            c, conn = connection()
            username = a['username']

            c.execute("SELECT * from Driver where username = %s ", [username])
            y = c.fetchone()
            conn.commit()
            c.close()
            gc.collect()
            d = {
                "full_name": y[0],
                "mobile_number": y[3],
                "license_number": y[1],
                "taxi_number": y[6]
            }
            onlinedriversinfo.append(d)

        return render_template("listofonlinedrivers.html", drivers=onlinedriversinfo)
    except Exception as e:
        return "error"


# Display online drivers on the map:

@app.route('/onlinedriversmap')
@login_required
def onlinedriversmap():
    try:
        c, conn = connection()
        c.execute("""SELECT * FROM OnlineDriver""")
        y = []
        x = c.fetchall()
        for row in x:
            username = row[0]
            c, conn = connection()
            c.execute("""SELECT * FROM Driver where username = %s""", [username])
            x = c.fetchone()
            conn.commit()
            c.close()
            gc.collect()
            full_name = x[0]
            address = x[2]
            mobile_number = x[3]
            photo_url = x[7]
            z = {
                'icon': '//maps.google.com/mapfiles/ms/icons/green-dot.png',
                'title': 'Driver Information',
                'lat': row[2],
                'lng': row[1],
                'infobox': (
                        "<b>Name:</b> " + full_name + "<br/>" +
                        "<b>Address:</b> " + address + "<br/>" +
                        "<b>Mobile Number:</b> " + mobile_number + "<br/>"
                                                                   "<img src = " + photo_url + " height=""126"" width=""150"">"
                )
            }
            y.append(z)

        conn.commit()
        c.close()

        gc.collect()

        fullmap = Map(
            identifier="fullmap",
            varname="fullmap",
            style=(
                "height:100%;"
                "width:100%;"
                "top:10;"
                "left:0;"
                "position:absolute;"
                "z-index:200;"
            ),
            lat=27.7,
            lng=85.2891,
            markers=y,
            maptype="TERRAIN",
            zoom="100"
        )
        return render_template('onlinedriversmap.html', fullmap=fullmap)
    except Exception as e:
        return "error"

import gc

from flask import request

from main import app


@app.route('/selectataxi', methods=['POST', 'GET'])
def selectataxi():
    try:
        if request.method == "POST":
            mobile_number = request.form['mobile_number']
            latitude = float(request.form['latitude'])
            longitude = float(request.form['longitude'])

        else:
            latitude = float(request.args['latitude'])
            longitude = float(request.args['longitude'])

        c, conn = connection()
        c.execute("SELECT * from OnlineCustomer where mobile_number = %s", [mobile_number])
        x = c.fetchone()
        c.close()
        conn.commit()
        gc.collect()

        if x:
            c, conn = connection()
            c.execute("DELETE from OnlineCustomer where mobile_number = %s", [mobile_number])
            c.close()
            conn.commit()
            gc.collect()

        else:
            pass

        c, conn = connection()
        c.execute("INSERT into OnlineCustomer values(%s,%s,%s)", (mobile_number, latitude, longitude))
        c.close()
        conn.commit()
        gc.collect()

        w = latitude + float(0.018087434)
        x = latitude - float(0.018087434)
        y = longitude + float(0.018087434)
        z = longitude - float(0.018087434)

        c, conn = connection()
        c.execute(
            """SELECT * FROM OnlineDriver WHERE longitude BETWEEN %s AND %s AND latitude BETWEEN %s AND %s and with_customer = %s """,
            (z, y, x, w, False))

        y = []
        x = c.fetchall()

        if len(x) == 0:
            return "No Drivers."

        for row in x:
            z = {
                "username": row[0],
                "longitude": row[1],
                "latitude": row[2]
            }
            y.append(z)

        w = {"markers": y}

        conn.commit()
        c.close()

        gc.collect()
        return json.dumps(w, indent=0)

    except Exception as e:
        return e

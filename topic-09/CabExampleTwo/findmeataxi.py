import gc

from flask import request, json

from distance import calculatedistance
from main import app


@app.route('/findmeataxi', methods=['POST'])
def findmeataxi():
    try:

        mobile_number = request.form['mobile_number']
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])

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

        x = c.fetchall()
        conn.commit()
        c.close()
        gc.collect()

        shortest_distance = 10000

        if len(x) == 0:
            return "No Drivers"

        for row in x:
            d = calculatedistance(longitude, latitude, row[1], row[2])
            if d < shortest_distance:
                shortest_distance = d
                nearest_user = row[0]

        c, conn = connection()
        c.execute("""SELECT * FROM Driver WHERE username = %s """, [nearest_user])
        x = c.fetchone()
        conn.commit()
        c.close()
        gc.collect()
        driver1 = []
        driver = {
            "full_name": x[0],
            "license_number": x[1],
            "address": x[2],
            "mobile_number": x[3],
            "taxi_number": x[6],
            "username": x[4]
        }

        driver1.append(driver)

        w = {"driver": driver1}
        return json.dumps(w, indent=0)

    except Exception as e:
        return e

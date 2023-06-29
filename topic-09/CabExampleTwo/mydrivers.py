import gc

from flask import request, json

from main import app


@app.route('/mydrivers', methods=["POST"])
def mydrivers():
    mobile_number = request.form['mobile_number']
    c, conn = connection()
    c.execute("SELECT * FROM Ride where mobile_number = %s)", [mobile_number])
    x = c.fetchall()
    conn.commit()
    c.close()
    gc.collect()

    driver = []
    for row in x:
        z = {
            "username": row[1],
            "timeofride": row[2]
        }
        driver.append(z)

    driversinfo = []
    for a in driver:
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
            "taxi_number": y[6],
            "timeofride": a['timeofride']
        }
        driversinfo.append(d)

    drivers = {"drivers": driversinfo}

    return json.dumps(drivers, indent=0)

import gc

from flask import request, json

from main import app


@app.route('/showprofile', methods=['POST'])
def showprofile():
    try:

        username = request.form['username']
        c, conn = connection()
        c.execute("SELECT * FROM Driver where username = %s", [username])
        x = c.fetchone()

        driver = []
        driver1 = {
            "full_name": x[0],
            "license_number": x[1],
            "address": x[2],
            "mobile_number": x[3],
            "taxi_number": x[6],
            "username": x[4]

        }
        driver.append(driver1)
        jsdriver = {"driver": driver}

        conn.commit()
        c.close()
        gc.collect()
        return json.dumps(jsdriver, indent=0)

    except Exception as e:
        return e

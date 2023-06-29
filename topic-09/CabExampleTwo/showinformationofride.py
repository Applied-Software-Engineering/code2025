import gc

from flask import request, json

from main import app


@app.route('/showinformationofride', methods=["POST"])
def showinformationofride():
    mobile_number = request.form['mobile_number']

    c, conn = connection()
    c.execute("SELECT * from Ride where mobile_number = %s ORDER BY timeofride DESC  ", [mobile_number])
    x = c.fetchone()
    conn.commit()
    c.close()
    gc.collect()
    informationofride2 = []
    informationofride1 = {
        "current_driver": x[0],
        "started_time": x[1],
        "distance": x[2],
        "duration_of_ride": x[3],
        "fare": x[4]
    }
    informationofride2.append(informationofride1)

    informationofride = {"informationofride": informationofride2}

    return json.dumps(informationofride, indent=0)

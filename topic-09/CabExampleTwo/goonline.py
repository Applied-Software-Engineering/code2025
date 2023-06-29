import gc

from flask import request

from main import app


@app.route('/goonline', methods=['POST'])
def goonline():
    username = request.form['username']
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])

    c, conn = connection()
    c.execute("SELECT * from OnlineDriver where username = %s", [username])
    x = c.fetchone()
    c.close()
    conn.commit()
    gc.collect()

    if x:
        c, conn = connection()
        c.execute("DELETE from OnlineDriver where username = %s", [username])
        c.close()
        conn.commit()
        gc.collect()

    c, conn = connection()
    c.execute("""INSERT INTO OnlineDriver (username,longitude,latitude,with_customer) VALUES (%s,%s,%s,%s)""",
              (username, longitude, latitude, False))
    conn.commit()
    c.close()

    gc.collect()
    return "online"


@app.route('/gooffline', methods=['POST'])
def gooffline():
    username = request.form['username']
    c, conn = connection()
    c.execute("""DELETE FROM OnlineDriver WHERE username = %s""", (username,))
    conn.commit()
    c.close()

    gc.collect()
    return "You went offline."

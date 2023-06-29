import gc

from flask import request

from main import app


@app.route('/updateme', methods=['POST'])
def updateme():
    username = request.form['username']
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    c, conn = connection()
    c.execute("DELETE from OnlineDriver where username = %s", [username])
    c.close()
    conn.commit()
    gc.collect()
    c, conn = connection()
    c.execute("""UPDATE OnlineDriver SET longitude =%s  , latitude =%s , with_costumer = %s WHERE username = %s""",
              (longitude, latitude, False, username,))
    conn.commit()
    c.close()

    gc.collect()
    return "Your location has been updated."

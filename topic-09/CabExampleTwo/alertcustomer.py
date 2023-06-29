import gc

from flask import request

from main import app


@app.route('/alertcustomer', methods=['POST'])
def alertcustomer():
    username = request.form['username']
    c, conn = connection()
    c.execute("SELECT * from Ride where username = %s ORDER BY timeofride DESC  ", [username])
    x = c.fetchone()
    conn.commit()
    c.close()
    gc.collect()
    mobile_number = x[4]

    return mobile_number

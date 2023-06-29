import gc

from flask import request

from main import app


@app.route('/completedaride', methods=['POST'])
def completedaride():
    username = request.form['username']
    distance = request.form['distance']
    time = request.form['time']
    fare = request.form['fare']

    c, conn = connection()
    c.execute("SELECT * from Ride where username = %s ORDER BY timeofride DESC  ", [username])
    x = c.fetchone()

    c.close()
    conn.commit()
    gc.collect()
    current_customer = x[5]

    c, conn = connection()
    c.execute("UPDATE Ride set distance = %s , time = %s , fare = %s where username = %s and mobile_number = %s ",
              (distance, time, fare, username, current_customer))
    conn.commit()
    c.close()
    gc.collect()

    c, conn = connection()
    c.execute("UPDATE OnlineDriver SET with_costumer = %s  WHERE username = %s ", (False, username))
    conn.commit()
    c.close()

    gc.collect()
    return "You completed a ride."

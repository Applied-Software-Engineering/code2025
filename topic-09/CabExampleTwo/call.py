import datetime
import gc

from flask import request

from main import app


@app.route('/callnow', methods=["POST"])
def callnow():
    if request.method == "POST":
        mobile_number = request.form['mobile_number']
        username = request.form['username']

    c, conn = connection()
    c.execute("""SELECT * FROM OnlineDriver WHERE username = %s and with_customer = %s""", (username, False))
    x = c.fetchone()
    conn.commit()
    c.close()

    c, conn = connection()
    c.execute("SELECT * from ForToken where username = %s", [username])
    x = c.fetchone()
    c.close()
    conn.commit()
    gc.collect()

    c, conn = connection()
    c.execute("""UPDATE OnlineDriver SET with_customer = %s where username = %s""", (True, username))
    c.close()
    conn.commit()

    c, conn = connection()
    timeofride = str(datetime.datetime.now())
    c.execute("INSERT INTO Ride (mobile_number, username, timeofride, status) values (%s,%s,%s,%s)",
              (mobile_number, username, timeofride, "UNKNOWN"))
    conn.commit()
    c.close()
    gc.collect()
    return "success"

@app.route('/callyes', methods=['POST'])
def callyes():
    username = request.form['username']

    c, conn = connection()
    c.execute("SELECT * from Ride where username = %s ORDER BY timeofride DESC  ", [username])
    x = c.fetchone()
    conn.commit()
    c.close()
    gc.collect()
    username = x[0]
    calledtimeofride = x[1]
    mobile_number = x[4]

    c, conn = connection()
    timeofride = datetime.datetime.now()
    c.execute("UPDATE Ride set status = %s WHERE username = %s and mobile_number = %s and timeofride = %s",
              ("ACCEPTED", username, mobile_number, calledtimeofride))
    conn.commit()
    c.close()
    gc.collect()

    return "callyes"


@app.route('/callno', methods=['POST'])
def callno():
    username = request.form['username']
    c, conn = connection()
    c.execute("SELECT * from Ride where username = %s ORDER BY timeofride DESC  ", [username])
    x = c.fetchone()
    conn.commit()
    c.close()
    gc.collect()

    username = x[0]
    calledtimeofride = x[1]
    mobile_number = x[4]

    c, conn = connection()
    c.execute("UPDATE Ride set status = %s WHERE username = %s and mobile_number = %s and timeofride = %s",
              ("CANCELLED", username, mobile_number, calledtimeofride))
    conn.commit()
    c.close()
    gc.collect()

    c, conn = connection()
    c.execute("""UPDATE OnlineDriver SET with_customer = %s where username = %s""", (False, username))
    c.close()
    conn.commit()

    return "callNo"

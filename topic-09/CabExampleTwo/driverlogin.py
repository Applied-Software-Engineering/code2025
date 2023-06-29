import gc

from flask import request

from main import app


@app.route('/driverlogin', methods=["POST"])
def driverlogin():
    username = request.form['username']
    password = request.form['password']
    token = request.form['token']

    c, conn = connection()
    c.execute("SELECT * from Driver where username = %s", [username])

    x = c.fetchone()
    c.close()
    conn.commit()
    gc.collect()

    if x:
        if x[5] == password:
            c, conn = connection()
            c.execute("SELECT * from ForToken where username =%s", [username])
            x = c.fetchone()
            c.close()
            conn.commit()
            gc.collect()

            if x:
                c, conn = connection()
                c.execute("DELETE from ForToken where username =%s", [username])
                c.close()
                conn.commit()
                gc.collect()

            c, conn = connection()
            c.execute("INSERT into ForToken (username, token) values(%s,%s)", (username, token))
            c.close()
            conn.commit()
            gc.collect()

            return "success"
        else:
            return "failed"

    else:
        return "Not a registered user"


@app.route('/driverlogout', methods=['POST'])
def driverlogout() -> str:
    username = request.form['username']
    c, conn = connection()
    c.execute("DELETE from ForToken where username = %s ", [username])
    conn.commit()
    c.close()
    gc.collect()
    return "logged out" + username

import gc

from flask import request

from main import app


@app.route('/driverforgotpassword', methods=['POST'])
def driverforgotpassword():
    username = request.form['username']
    c, conn = connection()
    c.execute("SELECT * from Driver where username = %s", [username])
    x = c.fetchone()
    conn.commit()
    c.close()
    gc.collect()

    if x:
        return "Password is sent to your mobile number."
    else:
        return "Your number is not registered."

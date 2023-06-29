import gc

from flask import request

from main import app


@app.route('/forgotpassword', methods=['POST'])
def forgotpassword():
    mobile_number = request.form['mobile_number']
    c, conn = connection()
    c.execute("SELECT * from Customer where mobile_number = %s", [mobile_number])
    x = c.fetchone()
    conn.commit()
    c.close()
    gc.collect()

    if x:
        return "Password is sent to your mobile number."
    else:
        return "Your number is not registered."

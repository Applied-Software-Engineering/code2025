import gc

from flask import request

from main import app


@app.route('/customerlogin', methods=["POST"])
def customerlogin():
    mobile_number = request.form['mobile_number']
    password = request.form['password']
    token = request.form['token']

    if mobile_number == "" or password == "":
        return "Enter Username and Password"

    else:
        pass

    c, conn = connection()
    c.execute("SELECT * from Block where mobile_number = %s", [mobile_number])
    x = c.fetchone()
    conn.commit()
    c.close()
    gc.collect()

    if x:
        return "Your number is in the Block List."

    c, conn = connection()
    c.execute("SELECT * from Customer where mobile_number = %s", [mobile_number])
    x = c.fetchone()
    c.close()
    conn.commit()
    gc.collect()

    if x:
        if x[2] == password:

            c, conn = connection()
            c.execute("SELECT * from ForCustomerToken where mobile_number =%s", [mobile_number])
            x = c.fetchone()
            c.close()
            conn.commit()
            gc.collect()

            if x:
                c, conn = connection()
                c.execute("DELETE from ForCustomerToken where mobile_number =%s", [mobile_number])
                c.close()
                conn.commit()
                gc.collect()

            c, conn = connection()
            c.execute("SELECT * from ForCustomerToken where token =%s", [token])
            x = c.fetchone()
            c.close()
            conn.commit()
            gc.collect()

            if x:
                c, conn = connection()
                c.execute("DELETE from ForCustomerToken where token =%s", [token])
                c.close()
                conn.commit()
                gc.collect()

            c, conn = connection()
            c.execute("INSERT into ForCustomerToken (mobile_number, token) values(%s,%s)", (mobile_number, token))
            c.close()
            conn.commit()
            gc.collect()

            return "success"
        else:
            return "failed"

    else:
        return "Username not correct"

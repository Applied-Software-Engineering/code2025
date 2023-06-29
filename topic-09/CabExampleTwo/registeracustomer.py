import gc

from flask import request

from main import app


@app.route('/registeracustomer', methods=["POST"])
def registeracustomer():
    full_name = request.form['full_name']
    mobile_number = request.form['mobile_number']
    password = request.form['password']
    code = int(request.form['code'])

    c, conn = connection()
    c.execute("SELECT * from ForCode WHERE mobile_number = %s", [mobile_number])
    x = c.fetchone()
    conn.commit()
    c.close()
    gc.collect()
    
    if int(x[1]) == code:
        c, conn = connection()
        c.execute("INSERT INTO Customer (full_name, mobile_number, password) VALUES (%s, %s, %s)",
                  (full_name, mobile_number, password))
        conn.commit()
        c.close()
        gc.collect()
        return "success"
    else:
        return "failed"

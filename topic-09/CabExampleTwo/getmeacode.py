import gc
from random import randint

from flask import request

from main import app


@app.route('/getmeacode', methods=['POST'])
def getmeacode():
    mobile_number = request.form['mobile_number']
    c, conn = connection()
    c.execute("SELECT * from Block where mobile_number = %s", [mobile_number])
    x = c.fetchone()
    conn.commit()
    c.close()
    gc.collect()

    if x:
        return "Your number is in the block list."

    else:
        c, conn = connection()
        c.execute("SELECT * from Customer where mobile_number = %s", [mobile_number])
        x = c.fetchone()
        conn.commit()
        c.close()
        gc.collect()

        if x:
            full_name = x[0]
            return "Your number is already registered in the name of " + full_name

        else:
            code = randint(10000, 99999)
            c = str(code)
            c, conn = connection()
            c.execute("DELETE from ForCode where mobile_number = %s", [mobile_number])
            conn.commit()
            c.close()
            gc.collect()
            c, conn = connection()
            c.execute("INSERT INTO ForCode (mobile_number, code) VALUES (%s,%s)", (mobile_number, code))
            conn.commit()
            c.close()
            gc.collect()
            return "success"

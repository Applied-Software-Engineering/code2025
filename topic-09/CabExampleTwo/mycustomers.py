import gc
from typing import Union, Any

from flask import request, json

from main import app


@app.route('/mycustomers', methods=["POST"])
def mycustomers():
    username = request.form['username']
    c, conn = connection()
    c.execute("SELECT * FROM Ride where username = %s", [username])
    x = c.fetchall()
    conn.commit()
    c.close()
    gc.collect()

    if len(x) == 0:
        return "Not a single ride"
    else:
        pass

    customer = []
    for row in x:
        z = {
            "mobile_number": row[4],
            "timeofride": str(row[1]),
            "status": row[6]
        }
        customer.append(z)

    customersinfo: list[dict[str, Union[str, Any]]] = []
    for a in customer:
        c, conn = connection()
        mobile_number = a['mobile_number']
        c.execute("SELECT * from Customer where mobile_number = %s ", [mobile_number])
        y = c.fetchone()
        c.close()
        conn.commit()
        gc.collect()
        m = {
            "full_name": y[0],
            "mobile_number": mobile_number,
            "timeofride": a['timeofride'],
            "status": a['status']
        }
        customersinfo.append(m)

    customers = {"customers": customersinfo}

    return json.dumps(customers, indent=0)

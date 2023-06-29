import gc

from flask import request, render_template

from main import app, login_required


@app.route('/listofcustomers', methods=['GET'])
@login_required
def listofcustomers_get():
    try:
        c, conn = connection()
        c.execute("SELECT * from Customer")
        customers = []
        x = c.fetchall()

        for row in x:
            z = {
                "full_name": row[0],
                "mobile_number": row[1]

            }
            customers.append(z)

        conn.commit()
        c.close()

        gc.collect()
        return render_template("listofcustomers.html", customers=customers)

    except Exception as e:
        return "error"


@app.route('/listofcustomers', methods=['POST'])
@login_required
def listofcustomers_post():
    try:

        info = request.form['x']
        c, conn = connection()
        c.execute("SELECT * from Customer where full_name = %s or mobile_number = %s", (info, info))
        customers = []

        x = c.fetchall()

        for row in x:
            z = {
                "full_name": row[0],
                "mobile_number": row[1]

            }
            customers.append(z)

        conn.commit()
        c.close()

        gc.collect()
        return render_template("listofcustomers.html", customers=customers)
    except Exception as e:
        return "error"

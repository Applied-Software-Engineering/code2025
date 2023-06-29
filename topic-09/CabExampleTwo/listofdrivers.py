from flask import request, render_template

from main import app, login_required


@app.route('/listofdrivers', methods=['GET', 'POST'])
@login_required
def listofdrivers():
    try:
        drivers = []
        if request.method == 'GET':
            c, conn = connection()
            c.execute("SELECT * from Driver ")
            x = c.fetchall()


            for row in x:
                z = {
                    "full_name": row[0],
                    "license_number": row[1],
                    "address": row[2],
                    "mobile_number": row[3],
                    "username": row[4],
                    "password": row[5],
                    "taxi_number": row[6]
                }
                drivers.append(z)

            conn.commit()
            c.close()
        else:  # POST
            info = request.form['x']
            c, conn = connection()
            c.execute(
                "SELECT * from Driver where full_name = %s or mobile_number = %s or taxi_number = %s or username = %s",
                (info, info, info, info))
            x = c.fetchall()

            for row in x:
                z = {
                    "full_name": row[0],
                    "license_number": row[1],
                    "address": row[2],
                    "mobile_number": row[3],
                    "username": row[4],
                    "password": row[5],
                    "taxi_number": row[6]
                }
                drivers.append(z)

            conn.commit()
            c.close()

        return render_template("listofdrivers.html", drivers=drivers)

    except Exception as e:
        return "error" # should return an error page and then go back to the login

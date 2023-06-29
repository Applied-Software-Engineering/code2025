import gc

from flask import render_template, request, flash, redirect, url_for

from main import app, login_required


@app.route('/update/<username>', methods=["POST"])
@login_required
def update_post(username):
    entered_license_number = request.form['license_number']
    entered_address = request.form['address']
    entered_mobile_number = request.form['mobile_number']
    entered_password = request.form['password']
    entered_taxi_number = request.form['taxi_number']

    c, conn = connection()
    c.execute("""Select * From Driver where mobile_number = %s""", [entered_mobile_number])
    x = c.fetchone()
    c.close()
    conn.commit()
    gc.collect()

    if x:
        flash("This Mobile Number is already taken")
        return render_template("register.html")

    c, conn = connection()
    c.execute("""Select * From Driver where taxi_number = %s""", [entered_taxi_number])
    x = c.fetchone()
    conn.commit()
    c.close()
    gc.collect()
    if x:
        flash("This Taxi Number is already taken")
        return render_template("register.html")

    c, conn = connection()
    c.execute(
        """UPDATE Driver SET license_number = %s , address  = %s , mobile_number  = %s , password  = %s , taxi_number  = %s where username = %s""",
        (entered_license_number, entered_address, entered_mobile_number, entered_password, entered_taxi_number,
         username))
    conn.commit()
    c.close()

    gc.collect()
    return redirect(url_for(".details", username=username))


@app.route('/update/<username>', methods=["GET"])
@login_required
def update_get(username):
    return render_template("update.html", username=username)

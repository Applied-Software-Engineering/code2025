from flask import request
from main import app
from main import login_required


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    try:

        if request.method == "POST":

            entered_full_name = request.form['full_name']
            entered_license_number = request.form['license_number']
            entered_address = request.form['address']
            entered_mobile_number = request.form['mobile_number']
            entered_username = request.form['username']
            entered_password = request.form['password']
            entered_taxi_number = request.form['taxi_number']
            file = request.files['file']

            c, conn = connection()
            c.execute("""Select * From Driver where mobile_number = %s""", [entered_mobile_number])
            x = c.fetchone()
            c.close()
            conn.commit()
            gc.collect()

            if x:
                flash("This Mobile Number is already taken")
                return render_template("register.html")

            else:
                pass

            c, conn = connection()
            c.execute("""Select * From Driver where username = %s""", [entered_username])
            x = c.fetchone()
            conn.commit()
            c.close()
            gc.collect()
            if x:
                flash("This Username is already taken")
                return render_template("register.html")

            else:
                pass

            c, conn = connection()
            c.execute("""Select * From Driver where taxi_number = %s""", [entered_taxi_number])
            x = c.fetchone()
            conn.commit()
            c.close()
            gc.collect()

            if x:
                flash("This Taxi Number is already taken")
                return render_template("register.html")

            else:
                pass

            if file:
                upload_result = upload(file, public_id=entered_username)
                photo_url1 = str(cloudinary_url(entered_username + ".jpg"))
                photo_url = photo_url1[2:-6]
                c, conn = connection()
                c.execute(
                    """INSERT INTO Driver (full_name,license_number,address,mobile_number,username,password,taxi_number,profile_photo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (
                        entered_full_name, entered_license_number, entered_address, entered_mobile_number,
                        entered_username,
                        entered_password, entered_taxi_number, photo_url))
                conn.commit()
                c.close()
                gc.collect()
                return redirect(url_for(".dashboard"))
            else:
                return render_template("register.html")
        else:
            return render_template("register.html")

    except Exception as e:
        return e

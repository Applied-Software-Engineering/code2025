import gc

from flask import render_template, request

from main import app, login_required


@app.route('/listofblockedcustomers')
@login_required
def listofblockedcustomer():
    try:

        c, conn = connection()
        c.execute("SELECT * from Block")
        blocked = []
        x = c.fetchall()
        conn.commit()
        c.close()
        gc.collect()
        for row in x:
            z = {
                "mobile_number": row[0]
            }
            blocked.append(z)

        blockedcustomers = []
        for a in blocked:
            c, conn = connection()
            mobile_number = a['mobile_number']

            c.execute("SELECT * from Customer where mobile_number = %s ", [mobile_number])
            y = c.fetchone()
            conn.commit()
            c.close()
            gc.collect()
            d = {
                "full_name": y[0],
                "mobile_number": y[1]
            }
            blockedcustomers.append(d)

        return render_template("listofblockedcustomer.html", blockedcustomers=blockedcustomers)

    except Exception as e:
        return "error"


@app.route('/listofrequestedblock/')
@login_required
def listofrequestedblock():
    try:

        c, conn = connection()
        c.execute("SELECT * from RequestToBlock")
        block = []
        x = c.fetchall()
        conn.commit()
        c.close()
        gc.collect()
        for row in x:
            z = {
                "mobile_number": row[0],
                "username": row[1]
            }
            block.append(z)

        info = []
        for a in block:
            mobile_number = a['mobile_number']
            username = a['username']
            c, conn = connection()
            c.execute("SELECT * from Customer where mobile_number = %s ", [mobile_number])
            y = c.fetchone()
            conn.commit()
            c.close()
            gc.collect()
            c, conn = connection()
            c.execute("SELECT * from Driver where username = %s ", [username])
            z = c.fetchone()
            conn.commit()
            c.close()
            gc.collect()
            d = {
                "full_name": y[0],

                "dfull_name": z[0]
            }
            info.append(d)

            # return json.dumps(info , indent = 0)
        return render_template("listofrequestedblock.html", info=info)

    except Exception as e:
        return "error"


@app.route('/requesttoblock', methods=['POST'])
def requesttoblock() -> str:
    username = request.form['username']
    mobile_number = request.form['mobile_number']
    c, conn = connection()
    c.execute("SELECT * from RequestToBlock where mobile_number = %s ", [mobile_number])
    x = c.fetchall()
    conn.commit()
    c.close()
    gc.collect()
    if len(x) == 4:
        c, conn = connection()
        c.execute("INSERT into Block (mobile_number) values (%s)", (mobile_number))
        conn.commit()
        c.close()
        gc.collect()
    else:
        c, conn = connection()
        c.execute("INSERT into RequestToBlock (mobile_number, requested_by) values (%s,%s)", (mobile_number, username))
        conn.commit()
        c.close()
        gc.collect()

    return "Your request to block " + mobile_number + "has been considered."

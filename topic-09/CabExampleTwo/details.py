import gc

from flask import render_template

from main import app, login_required


@app.route('/details/<username>')
@login_required
def details(username):
    c, conn = connection()
    c.execute("SELECT * from Driver where username = %s ", [username])
    x = c.fetchone()
    conn.commit()
    c.close()
    gc.collect()
    photo_url = x[7]
    return render_template("details.html", driver=x, photo_url=photo_url)


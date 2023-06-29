import gc

from flask import render_template, redirect, url_for

from main import app, login_required


@app.route('/delete/<username>')
@login_required
def delete(username):
    c, conn = connection()
    c.execute("SELECT * from Driver where username = %s ", [username])
    x = c.fetchone()
    conn.commit()
    c.close()
    gc.collect()
    return render_template("delete.html", driver=x)


@app.route('/finaldelete/<username>')
@login_required
def finaldelete(username):
    c, conn = connection()
    c.execute("DELETE from Driver where username = %s ", [username])
    conn.commit()
    c.close()
    gc.collect()
    return redirect(url_for(".listofdrivers"))


import gc

from flask import request

from main import app


@app.route('/gotapassenger', methods=['POST'])
def gotapassenger():
    username = request.form['username']
    c, conn = connection()
    c.execute("UPDATE OnlineDriver SET with_costumer = %s  WHERE username = %s ", (True, username))
    c.close()
    conn.commit()
    gc.collect()
    return "You have a costumer"

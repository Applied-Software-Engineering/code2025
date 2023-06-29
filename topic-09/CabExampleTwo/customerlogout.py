import gc

from flask import request

from main import app


@app.route('/customerlogout', methods=['POST'])
def customerlogout():
    mobile_number = request.form['mobile_number']
    c, conn = connection()
    c.execute("DELETE from ForToken where mobile_number = %s ", [mobile_number])
    conn.commit()
    c.close()
    gc.collect()
    return "logged out"

from flask import request, render_template, redirect, url_for, session
from main import app

@app.route("/", methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']
            users = [{"username": "admin", "password": "admin"},
                     {"username": "admin2", "password": "dogs"}]

            for i in users:
                if attempted_username == i['username'] and attempted_password == i['password']:
                    #session['username'] = attempted_username
                    #session['logged_in'] = True
                    print(f"Sess: {session}")
                    print(f"url:") #{url_for('dashboard.html')}")
                    return redirect(url_for("dashboard.html"))
        return render_template("login.html")
    except Exception as e:
        return render_template("login.html")

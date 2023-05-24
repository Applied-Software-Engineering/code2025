import os
from random import shuffle

from flask import Flask, render_template, redirect, url_for, request
from markupsafe import escape
from data_manager import SimpleDataManager

db_filename = os.path.join('res', 'user_db.db')
csv_users_filename = os.path.join('res', 'full_user_data.csv')

app = Flask(__name__)
data = SimpleDataManager()
# data.load_users(os.path.join('res', 'user_data.csv'))
data.load_user_from_db(csv_users_filename, db_filename)

@app.route('/', methods=(['POST', 'GET']))
@app.route('/index', methods=(['POST', 'GET']))
def get_home_page():
    if request.method == 'POST':
        user = escape(request.form['name'])
        if user.title() in data.users:
            return redirect(url_for('get_user_page', username=user.lower()))
        else:
            return redirect(url_for('get_new_user_page'))
    return render_template('index.html', title='Home Page')

@app.route('/about')
def get_about_page():
    users = []
    for _ in range(3):
        shuffle(data.users)
        users = data.users[:3]

    return render_template('about.html', title='Home Page', users=users)


@app.route('/warn')
def get_warning_page(message=''):
    return render_template('error_page.html', title='Error Page', message=message)


@app.route('/user/<string:username>')
def get_user_page(username):
    safe_username = escape(username).strip()
    if safe_username == 'all_users':
        return redirect(url_for("get_all_users_page"))
    if not safe_username.title() in data.users:
        return redirect(url_for('get_warning_page'))

    return render_template('user_page.html', title='User Page' ,username=safe_username)


@app.route('/all_users')
def get_all_users_page():
    return render_template("all_users.html", title="All Users Page", users=data.users)


@app.route('/new_user', methods = ([ 'POST','GET']))
def get_new_user_page():
    if request.method == 'POST':
        new_user = escape(request.form['name']).title()
        new_location = escape(request.form['location']).title()
        new_club = escape(request.form['club']).title()
        if new_user in data.users or new_user == '':
            return render_template('add_new_user_page.html')
        data.users.append(new_user)
        conn = data.get_db_connection(db_filename)
        conn.execute(f'insert into users values("{new_user}", "{new_location}", "{new_club}");')
        return redirect(url_for ('get_user_page', username=new_user.lower()))
    return render_template('add_new_user_page.html', title="New User Page")

if __name__ == "__main__":
    # app.run()

    # Optional, host address often required if running on a VM
    app.run(debug=True, host="0.0.0.0")
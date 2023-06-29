from flask import render_template, session

from main import app, login_required


@app.route('/dashboard')
@login_required
def dashboard():
    try:
        username = session['username']
        return render_template('dashboard.html', username=username)
    except Exception as e:
        return "error"

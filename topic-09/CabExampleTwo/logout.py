from flask import redirect, url_for

from main import app, login_required


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    return redirect(url_for('login'))

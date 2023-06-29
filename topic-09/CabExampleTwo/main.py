from flask import Flask, url_for, redirect, session
from functools import wraps
from flask_googlemaps import GoogleMaps

from db import engine, SQLModel

app = Flask(__name__)

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4"

# you can also pass key here
GoogleMaps(app, key="AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4")


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login"))

    return wrap


import register
import login
import logout
import dashboard
import listofdrivers
import listofcustomers
import delete
import details
import update
import listofonlinedrivers
import blockcustomer
import forgotpassword
import registeracustomer
import customerlogin
import selectataxi
import findmeataxi
import showprofile
import mydrivers
import showinformationofride
import customerlogout
import driverlogin
import driverforgotpassword
import goonline
import gotapassenger
import completedaride
import call
import alertcustomer
import updateme
import mycustomers
import blockcustomer

if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
    app.run(debug=True, use_reloader=True, use_debugger=True)

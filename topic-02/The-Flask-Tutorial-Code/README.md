# Flaskr


The basic blog app code for the Flask tutorial.

... tutorial source: https://flask.palletsprojects.com/tutorial/

## Setup

Install the `flask` package.

## Run the app

```
    $ export FLASK_APP=flaskr
    $ export FLASK_ENV=development
    $ flask init-db
    $ flask run --host=0.0.0.0
```

Or on Windows cmd::

```
    > set FLASK_APP=flaskr
    > set FLASK_ENV=development
    > flask init-db
    > flask run
```

On Windows, open http://127.0.0.1:5000 in a browser.


## Testing

```
    $ pip install '.[test]'
    $ pytest
```

Run with coverage report

```
    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser
```    

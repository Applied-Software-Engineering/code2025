import sqlalchemy as db
from sqlalchemy.orm import Session
from sqlalchemy import text, select

if __name__ == "__main__":
    engine = db.create_engine("sqlite:///european_database.sqlite", echo=True)
    session = Session(engine)
    stmt = select(text("name")).select_from(text("divisions"))
    result = session.execute(stmt)
    for divs in result.all():
        print(divs)

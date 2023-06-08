from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select


class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None


person_1 = Person(name="Fred", age=42)
person_2 = Person(name="Harry", age=45)
person_3 = Person(name="Mary", age=25)

database_name = "database.db"
engine = create_engine(f"sqlite:///{database_name}")


SQLModel.metadata.create_all(engine)

session = Session(engine)

session.add(person_1)
session.add(person_2)
session.add(person_3)

session.commit()

with Session(engine) as sess:
    statement = select(Person).where(Person.name == "Harry").where(Person.age > 40)
    result = sess.exec(statement)
    for person in result:
        print(person)

session.close()

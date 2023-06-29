import os

from sqlmodel import create_engine, SQLModel

DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///taxi.db')

engine = create_engine(DATABASE_URI, echo=True)
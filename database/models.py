
from peewee import Model, SqliteDatabase, CharField, DateTimeField, ForeignKeyField, TextField, BooleanField
import datetime
import os

db = SqliteDatabase('alerts.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField(unique = True)
    CreatedField = DateTimeField(default = datetime.datetime.now)

class Alert(BaseModel):
    user = ForeignKeyField(User, null=True, backref="alerts")
    timestampField = DateTimeField()
    message = TextField()
    source = CharField(null = True)
    hidden = BooleanField(default=False)
    




def init_db():
    if db.is_closed():
        db.connect()
    db.create_tables([Alert, User], safe=True)
    print("[DEBUG] Baza danych zainicjalizowana.")
    

init_db()

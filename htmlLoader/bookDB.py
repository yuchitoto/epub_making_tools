import peewee
from peewee import *


db = MySQLDatabase(database='book', user='root', password='some_password', host='localhost', port=3306)


class BaseModel(Model):
    class Meta:
        database = db

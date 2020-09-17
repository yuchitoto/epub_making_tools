import peewee
from peewee import *
from bookDB import BaseModel


"""
BaseModel is for database connection
Please use the one on peewee as reference
"""


def id_to_array(data):
    return list(map(lambda x: x[0], data))


class wenku8(BaseModel):
    id = IntegerField(primary_key=True)
    book_name = CharField()
    author = CharField()
    publisher = CharField()
    available = BooleanField()
    last_update = DateField()
    local_update = DateTimeField()


    def containedID():
        tmp = wenku8.select(wenku8.id).tuples()
        return id_to_array(tmp)


    def availableID():
        tmp = wenku8.select(wenku8.id).where(wenku8.available=='true').tuples()
        return id_to_array(tmp)


    def crabbedID():
        tmp = wenku8.select(wenku8.id).where(wenku8.available=='false').tuples()
        return id_to_array(tmp)

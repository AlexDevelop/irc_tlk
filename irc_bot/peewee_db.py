import peewee
from datetime import datetime as dt, timedelta

db = peewee.MySQLDatabase('tlk', user='tlk', passwd='tlk1')
db.commit_select = True

class Todos_Todolist(peewee.Model):
    id = peewee.PrimaryKeyField()
    created = peewee.DateTimeField()
    modified = peewee.DateTimeField()
    name = peewee.CharField()
    description = peewee.CharField()
    data = peewee.TextField()
    date_deadline = peewee.DateTimeField()
    todo_type_id = peewee.IntegerField()
    identifier = peewee.IntegerField()
    status = peewee.IntegerField()

    class Meta:
        database = db


todos = Todos_Todolist.select().where(Todos_Todolist.status == False, Todos_Todolist.todo_type_id == 1).order_by(Todos_Todolist.identifier.desc())
todos_pvp = Todos_Todolist.select().where(Todos_Todolist.status == False, Todos_Todolist.todo_type_id == 2).order_by(Todos_Todolist.identifier.desc())

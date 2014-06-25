import datetime

import peewee

from peewee import IntegerField
from peewee import FloatField
from peewee import CharField
from peewee import TextField
from peewee import DateField
from peewee import DateTimeField
from peewee import ForeignKeyField

from .core import get_hash


database = peewee.Proxy()


class BaseModel(peewee.Model):
    @classmethod
    def check(cls, *args, **kwargs):
        try:
            cls.get(*args, **kwargs)
        except cls.DoesNotExist:
            return False
        else:
            return True

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.id)

    class Meta:
        database = database


class User(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def auth(cls, name, password):
        return User.get(name=name, password=get_hash(password))

    @classmethod
    def register(cls, name, password, email):
        return User.create(name=name, email=email, password=get_hash(password))

    def __repr__(self):
        return '<User %r>' % self.name

    class Meta:
        order_by = ('name',)


class _List(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(unique=True)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.name)


class Type(_List):
    pass


class Category(_List):
    pass


class Transaction(BaseModel):
    id = IntegerField(primary_key=True)
    user = ForeignKeyField(User, related_name='transactions')
    type = ForeignKeyField(Type, related_name='transactions')
    date = DateField(default=datetime.date.today())
    category = ForeignKeyField(Category, related_name='transactions')
    value = FloatField()
    description = TextField(null=True)

    @classmethod
    def delete_user_transaction(cls, user, transaction_id):
        transaction = Transaction.get(id=transaction_id)

        if transaction.user == user:
            transaction.delete_instance()
            return True

        return False

    class Meta:
        order_by = ('-date',)

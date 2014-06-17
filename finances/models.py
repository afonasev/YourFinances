import uuid
import hashlib
import datetime

import peewee

from peewee import IntegerField
from peewee import FloatField
from peewee import CharField
from peewee import TextField
from peewee import DateTimeField
from peewee import ForeignKeyField


database = peewee.Proxy()


class BaseModel(peewee.Model):
    class Meta:
        database = database


class User(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    password = CharField()
    salt = CharField(default=str(uuid.uuid4()))
    join_date = DateTimeField(default=datetime.datetime.now)

    class AuthError(Exception):
        pass

    class RegisterError(Exception):
        pass

    @classmethod
    def auth(cls, name, password):
        user = User.get(name=name)

        pass_with_salt = password + user.salt
        pass_hash = hashlib.sha224(pass_with_salt.encode()).hexdigest()

        if not pass_hash == user.password:
            raise cls.AuthError('Wrong password!')

        return user

    @classmethod
    def register(cls, name, password):
        try:
            User.get(name=name)
            raise cls.RegisterError('User with that name does exist')
        except User.DoesNotExist:
            pass

        user = User(name=name)
        pass_with_salt = password + user.salt
        user.password = hashlib.sha224(pass_with_salt.encode()).hexdigest()
        user.save()

    def __repr__(self):
        return '<User %r>' % self.name

    class Meta:
        order_by = ('name',)


class _Category(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(unique=True)

    def __repr__(self):
        return '<%s %r>' % (self.__name__, self.name)


class Category(_Category):
    pass


class SubCategory(_Category):
    pass


class Transaction(BaseModel):
    id = IntegerField(primary_key=True)
    category = ForeignKeyField(Category, related_name='transactions')
    sub_category = ForeignKeyField(SubCategory, related_name='transactions')
    date = DateTimeField(default=datetime.datetime.now)
    value = FloatField()
    description = TextField()

    def __repr__(self):
        return '<Transaction %r>' % self.id

    class Meta:
        order_by = ('-date',)

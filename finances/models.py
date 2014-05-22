import os
import hashlib
import datetime

import peewee


database = peewee.Proxy()


class BaseModel(peewee.Model):
    class Meta:
        database = database


class User(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField(unique=True)
    password = peewee.CharField()
    salt = peewee.CharField(default=os.urandom(10).decode('cp1251', errors='replace'))
    join_date = peewee.DateTimeField(default=datetime.datetime.now)

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


class CategoryType(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField()

    def __repr__(self):
        return '<CategoryType %r>' % self.name


class Category(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    name = peewee.CharField()
    type = peewee.ForeignKeyField(CategoryType, related_name='categories')

    def __repr__(self):
        return '<Category %r>' % self.name

    class Meta:
        order_by = ('name',)


class Transaction(BaseModel):
    id = peewee.IntegerField(primary_key=True)
    category = peewee.ForeignKeyField(Category, related_name='transactions')
    value = peewee.FloatField()
    description = peewee.TextField()
    need = peewee.ForeignKeyField(Category, related_name='transactions')
    date = peewee.DateTimeField(default=datetime.datetime.now)

    def __repr__(self):
        return '<Transaction %r>' % self.id

    class Meta:
        order_by = ('-date',)

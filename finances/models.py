import datetime

import peewee as pw

from . import validators
from .utils import get_hash
from .utils import ApplicationError


database = pw.Proxy()


class _BaseModel(pw.Model):

    @classmethod
    def _check(cls, *args, **kwargs):
        try:
            cls.get(*args, **kwargs)
        except cls.DoesNotExist:
            return False
        else:
            return True

    def __repr__(self):
        attrs = self.__dict__['_data'].copy()
        pairs = ['id:%s' % attrs.pop('id')]
        pairs += ['%s:%s' % (k, v) for k, v in attrs.items()]
        return '<%s {%s}>' % (self.__class__.__name__, ', '.join(pairs))

    class AccessError(ApplicationError):
        pass

    class UniqueError(ApplicationError):
        pass

    class ValidationError(ApplicationError):
        pass

    class Meta:
        database = database


class User(_BaseModel):
    email = pw.CharField()
    password = pw.CharField()

    @property
    def transactions(self):
        return Transaction.select().where(
            (Transaction.source << self.accounts) |
            (Transaction.target << self.accounts)
        )

    @classmethod
    @validators.email_pass_empty
    def auth(cls, email, password):
        if not User._check(email=email, password=get_hash(password)):
            raise cls.AuthError('Wrong email or password')
        return User.get(email=email, password=get_hash(password))

    @classmethod
    @validators.email_pass_empty
    @validators.email_pass_correct
    def reg(cls, email, password):
        if User._check(email=email):
            raise cls.RegError('User with same email already exists')
        return User.create(email=email, password=get_hash(password))

    class AuthError(ApplicationError):
        pass

    class RegError(ApplicationError):
        pass


class Account(_BaseModel):
    name = pw.CharField()
    owner = pw.ForeignKeyField(User, related_name='accounts')
    balance = pw.FloatField(default=0)
    is_personal = pw.BooleanField(default=False)

    @property
    def transactions(self):
        return Transaction.select().where(
            (Transaction.target == self) |
            (Transaction.source == self)
        )

    @classmethod
    def reg(cls, owner, name, is_personal=True):
        if not name:
            raise cls.ValidationError('Account name is empty')

        if Account._check(owner=owner, name=name):
            raise cls.UniqueError('Account with same name already exists')
        return Account.create(owner=owner, name=name, is_personal=is_personal)


class Transaction(_BaseModel):
    source = pw.ForeignKeyField(Account, related_name='subtractions')
    target = pw.ForeignKeyField(Account, related_name='additions')
    amount = pw.FloatField()
    description = pw.CharField(null=True)
    date = pw.DateTimeField(default=datetime.datetime.now)

    @classmethod
    @validators.target_source_owner
    def reg(cls, creator, source, target, amount, description=None, date=None):
        if source == target:
            raise cls.ValidationError(
                'Source account must be not equal target account'
            )

        if not amount:
            raise cls.ValidationError('Amount must be not equal zero')

        transaction = {
            'source': source,
            'target': target,
            'amount': amount,
            'description': description,
        }

        if amount < 0:
            transaction['source'], transaction['target'] = target, source
            amount *= -1

        if date:
            transaction['date'] = date

        source.balance -= amount
        target.balance += amount
        source.save()
        target.save()

        return Transaction.create(**transaction)


import peewee as pw

from . import validators
from .utils import get_hash, ApplicationError


database = pw.Proxy()


class BaseModel(pw.Model):

    @classmethod
    def _check(cls, *args, **kwargs):
        try:
            cls.get(*args, **kwargs)
        except cls.DoesNotExist:
            return False
        else:
            return True

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.id)

    class UniqueError(ApplicationError):
        pass

    class ValidationError(ApplicationError):
        pass

    class Meta:
        database = database


class User(BaseModel):
    email = pw.CharField()
    password = pw.CharField()

    @classmethod
    @validators.email_pass_empty
    def auth(cls, email, password):
        if not User._check(email=email, password=password):
            raise cls.AuthError('Wrong email or password')
        return User.get(email=email, password=get_hash(password))

    @classmethod
    @validators.email_pass_empty
    @validators.email_pass_correct
    def reg(cls, email, password):
        if User._check(email=email):
            raise cls.RegError('User with this email already exists')
        return User.create(email=email, password=get_hash(password))

    def __repr__(self):
        return '<User %r %r>' % (self.id, self.email)

    class AuthError(ApplicationError):
        pass

    class RegError(ApplicationError):
        pass


class Account(BaseModel):
    name = pw.CharField()
    owner = pw.ForeignKeyField(User, related_name='accounts')
    balance = pw.IntegerField(default=0)
    is_personal = pw.BooleanField(default=False)

    @classmethod
    def reg(cls, owner, name, is_personal):
        if not name:
            cls.ValidationError('Account name is empty')

        if Account._check(owner=owner, name=name):
            raise cls.UniqueError('Account with this name already exists')
        return Account.create(owner=owner, name=name, is_personal=is_personal)

    def __repr__(self):
        return '<Account %r %r>' % (self.id, self.name)

    class Meta:
        order_by = ('-is_personal', )

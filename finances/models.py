
import peewee as pw

from .utils import get_hash


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

    class UniqueError(Exception):
        pass

    class Meta:
        database = database


class User(BaseModel):
    email = pw.CharField()
    password = pw.CharField()

    @classmethod
    def auth(cls, email, password):
        return User.get(email=email, password=get_hash(password))

    @classmethod
    def reg(cls, email, password):
        if User._check(email=email):
            raise cls.UniqueError
        return User.create(email=email, password=get_hash(password))

    def __repr__(self):
        return '<User %r %r>' % (self.id, self.email)


class Account(BaseModel):
    name = pw.CharField()
    owner = pw.ForeignKeyField(User, related_name='accounts')
    balance = pw.IntegerField(default=0)
    is_personal = pw.BooleanField(default=False)

    @classmethod
    def reg(cls, owner, name, is_personal):
        if Account._check(owner=owner, name=name):
            raise cls.UniqueError
        return Account.create(owner=owner, name=name, is_personal=is_personal)

    def __repr__(self):
        return '<Account %r %r>' % (self.id, self.name)

    class Meta:
        order_by = ('-is_personal', )

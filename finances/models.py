
import peewee as pw

from .utils import get_hash


database = pw.Proxy()


class BaseModel(pw.Model):
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
    id = pw.IntegerField(primary_key=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()

    @classmethod
    def auth(cls, email, password):
        return User.get(email=email, password=get_hash(password))

    @classmethod
    def register(cls, email, password):
        return User.create(email=email, password=get_hash(password))

    def __repr__(self):
        return '<User %r>' % self.email

    class Meta:
        order_by = ('email',)

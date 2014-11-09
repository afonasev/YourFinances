import re


def email_pass_empty(func):
    def wrapper(cls, email, password, *args, **kwargs):
        if not email:
            raise cls.ValidationError('Email is empty')

        if not password:
            raise cls.ValidationError('Password is empty')

        return func(cls, email, password, *args, **kwargs)
    return wrapper


def email_pass_correct(func):
    def wrapper(cls, email, password, *args, **kwargs):
        if not is_correct_email(email):
            raise cls.ValidationError('Email is not correct')

        if len(password) < 6:
            raise cls.ValidationError(
                'Length of the password must be greater than 5 letters'
            )

        if not re.search('\d+', password):
            raise cls.ValidationError('The password should contain numbers')

        if not re.search('[a-zA-Z]+', password):
            raise cls.ValidationError('The password should contain letters')

        return func(cls, email, password, *args, **kwargs)
    return wrapper


def is_correct_email(email):
    return bool(re.search('.+@.+\..+', email))


def target_source_owner(func):
    def wrapper(cls, creator, source, target, *args, **kwargs):
        if source.owner != creator:
            raise cls.AccessError('User does not own source account')

        if target.owner != creator:
            raise cls.AccessError('User does not own target account')

        return func(cls, creator, source, target, *args, **kwargs)
    return wrapper

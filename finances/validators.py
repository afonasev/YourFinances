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
                'Length of password must be greater than 5 letters'
            )

        if not re.search('\d+', password):
            raise cls.ValidationError('The password should contain numbers')

        if not re.search('[a-zA-Z]+', password):
            raise cls.ValidationError('The password should contain letters')

        return func(cls, email, password, *args, **kwargs)
    return wrapper


def is_correct_email(email):
    return bool(re.search('.+@.+\..+', email))

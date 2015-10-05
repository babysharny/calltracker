from flask_wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required, Length, ValidationError

class LoginForm(Form):
    """docstring for LoginForm"""
    openid = TextField('openid', validators = [Required()])
    email = TextField('email')    
    pwd = TextField('pwd')
    pwd.validators = None
    remember_me = BooleanField('remember_me', default = True)

    def validate_email(form, field):
        if len(field.data) < 3:
            raise ValidationError('Custom validate')

    def validate_pwd(form, field):
        i_want = False
        if i_want:
            raise ValidationError('I Want Password')
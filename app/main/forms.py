from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms.validators import DataRequired
from ..models import User, Role

class PostForm(FlaskForm):
    #body = TextAreaField("What's on your mind?", validators=[DataRequired()])
    body = PageDownField("你在想什么?", validators=[DataRequired()])
    submit = SubmitField('发布')

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('确认')

class EditProfileForm(FlaskForm):
    name = StringField('姓名', validators=[Length(0, 64)])
    location = StringField('坐标', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('保存')

class EditProfileAdminForm(FlaskForm):
    email = StringField(
        'Email', 
        validators=[
            DataRequired(), 
            Length(1, 64),
            Email()
        ]
    )
    username = StringField(
        'Username', 
        validators=[
            DataRequired(), 
            Length(1, 64), 
            Regexp(
                '^[A-Za-z][A-Za-z0-9_.]*$', 
                0,
                'Usernames must have only letters,numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('保存')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [
            (role.id, role.name) for role in Role.query.order_by(Role.name).all()
        ]
        self.user = user
    
    def validate_email(self, field):
        if field.data != self.user.email and \
            User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    
    def validate_username(self, field):
        if field.data != self.user.username and \
            User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
                
class CommentForm(FlaskForm):
    body = StringField('', validators=[DataRequired()])
    submit = SubmitField('发表')
                                                     

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


from utils.validators import valid_username


class NewUsernameForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), valid_username])

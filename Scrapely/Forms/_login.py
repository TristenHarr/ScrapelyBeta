from wtforms import Form, StringField, PasswordField, validators


class LoginForm(Form):
    """
    The login form built using WTForms
    """
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])

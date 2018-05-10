from wtforms import Form, StringField, PasswordField, BooleanField, validators


class RegistrationForm(Form):
    """
    The registration form built using WTForms
    """
    username = StringField('Username', [validators.Length(min=4, max=25), validators.InputRequired()])
    email = StringField("Email Address", [validators.Email(), validators.InputRequired()])
    password = PasswordField("Password", [validators.InputRequired(),
                                          validators.EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('Confirm Password', [validators.InputRequired()])
    accept_tos = BooleanField('I accept the Terms and Conditions', [validators.DataRequired()])

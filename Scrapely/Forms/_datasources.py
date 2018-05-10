from wtforms import StringField, validators, Form


class TwitterForm(Form):
    """
    The form used to collect the keys required to connect to twitter via OAuth2
    """
    access_token = StringField('Access Token', [validators.InputRequired()])
    access_token_secret = StringField('Access Token Secret', [validators.InputRequired()])
    consumer_key = StringField('Consumer Key', [validators.InputRequired()])
    consumer_secret = StringField('Consumer Secret', [validators.InputRequired()])

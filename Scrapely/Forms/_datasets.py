from wtforms import Form, IntegerField, RadioField, TextAreaField, StringField, PasswordField, SelectField, validators
from flask import session


class ScrapeKeywordsForm(Form):
    """
    The form used to collect the information needed to run the twitter scraper in "track" mode
    """
    # TODO: Add the ability to search by language
    limit = IntegerField("Limit", [validators.InputRequired(),
                                   validators.NumberRange(min=1, max=1000, message="Current limit exceeded")])
    limit_type = RadioField("Limit Type", [validators.InputRequired()],
                            choices=[("TIME", "Seconds"), ("COUNT", "Tweets")])
    keywords = TextAreaField("Keywords, separated by a comma", [validators.InputRequired()])
    table = StringField("Table Name", [validators.InputRequired(), validators.Length(min=1, max=25)])
    password = PasswordField("Confirm Password", [validators.InputRequired()])


class ExportForm(Form):
    table = SelectField("Table Name", [validators.InputRequired()],
                        choices=[(table[0], table[0]) for table in session['table_count_keywords']])
    choice = RadioField("Export As", [validators.InputRequired()],
                        choices=[('csv', 'CSV'),
                        ('json', "JSON"),
                        ("excel", "Excel"),
                        ("html", "html"),
                        ("LaTeX", "LaTeX")])

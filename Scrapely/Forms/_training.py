from wtforms import Form, IntegerField, RadioField, TextAreaField, StringField, PasswordField, SelectField, validators,FieldList, FormField
from flask import session


class MultiBayesForm(Form):
    traininga = SelectField("Training Set A", [validators.InputRequired()],
                        choices=[(table[0], table[0]) for table in session['table_count_keywords']])
    trainingb = SelectField("Training Set B", [validators.InputRequired()],
                        choices=[(table[0], table[0]) for table in session['table_count_keywords']])


class MultiBayesTest(Form):
    controla = SelectField("Control A", [validators.InputRequired()],
                           choices=[(table[0], table[0]) for table in session['table_count_keywords']])
    controlb = SelectField("Control B", [validators.InputRequired()],
                           choices=[(table[0], table[0]) for table in session['table_count_keywords']])
    testinga = SelectField("Data In Category A", [validators.InputRequired()],
                           choices=[(table[0], table[0]) for table in session['table_count_keywords']])
    testingb = SelectField("Data In Category B", [validators.InputRequired()],
                           choices=[(table[0], table[0]) for table in session['table_count_keywords']])


class TableTestingForm(Form):
    name = IntegerField()

class MultiBayesMultiTest(Form):
    controls = FieldList(FormField(TableTestingForm), min_entries=2, max_entries=10)
    controla = SelectField("Control A", [validators.InputRequired()],
                           choices=[(table[0], table[0]) for table in session['table_count_keywords']])
    controlb = SelectField("Control B", [validators.InputRequired()],
                           choices=[(table[0], table[0]) for table in session['table_count_keywords']])



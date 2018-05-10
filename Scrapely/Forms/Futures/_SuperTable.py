from wtforms import Form, SelectField, StringField, RadioField, PasswordField, validators
from flask import session

class DropForm(Form):
    droptype = RadioField("Drop By", [validators.InputRequired()],
                        choices=[('row', 'Row'),
                        ('col', "Column")])
    dropselection = StringField("Drop Index:", [validators.InputRequired()])

class SwapForm(Form):
    swaptype = RadioField("Swap Axis:", [validators.InputRequired()],
                        choices=[('row', 'Row'),
                        ('col', "Column")])
    swapselection1 = StringField("Item 1 Index:", [validators.InputRequired()])
    swapselection2 = StringField("Item 2 Index:", [validators.InputRequired()])

class TableForm(Form):
    table = SelectField("Table", [validators.InputRequired()],
                        choices=[(table[0], table[0]) for table in session['table_count_keywords']])

class SaveNew(Form):
    name = StringField("New Table Name:", [validators.InputRequired()])

class PushForm(Form):
    password = PasswordField("Password", [validators.InputRequired()])

class NewRow(Form):
    datatype = RadioField("DataType", [validators.InputRequired()],
                        choices=[('INTEGER', 'Integer'),
                                 ('VARCHAR', "Varchar"),
                                 ("BLOB", "Blob"),
                                 ("TEXT", "Text")])
    rowname = StringField("New Row Name:", [validators.InputRequired()])
    backfill = StringField("Fill Old Columns with:", [validators.InputRequired()])

class NewColumn(Form):
    # Get the current columns somehow
    pass

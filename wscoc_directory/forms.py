from flask_wtf import FlaskForm
from wtforms import TextAreaField, FieldList
#from wtforms.widgets import TextArea
from wtforms.validators import DataRequired

class EmailForm(FlaskForm):
    master_list = TextAreaField(u'Master List', [DataRequired()])
    contacts_list = TextAreaField(u'Contacts List', [DataRequired()])
    group_list = FieldList(TextAreaField(u'Group List', [DataRequired()]), min_entries=5)
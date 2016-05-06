# -*- coding: utf-8 -*- 
from wtforms import Form, BooleanField, TextField, validators, FieldList, IntegerField,TextAreaField,Field
from wtforms.widgets import TextInput 

class TagListField(TextField):
    widget = TextInput()
    def __init__(self, label='Authors', **kwargs):
       super(TagListField, self).__init__(label, **kwargs)

    def _value(self):
        if self.data:
            return ', '.join(repr(item) for item in self.data)
        else:
            return ''
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []


class AuthorForm(Form):
    name = TextField('Authors name', [validators.required(message='name is required'),validators.Length(message='username between 4 and 8 symbols.',min=4, max=30 )])
class BookForm(Form):
    name = TextField('Title', [validators.required(message='Title is required'),validators.Length(message='username between 4 and 8 symbols.',min=4, max=160 )])
    authors = TagListField(TextField('Authors'))#, validators=[validators.required(message='Author is required')]))
    description = TextAreaField('Book description', [validators.optional(),validators.length(message='not more than 500 symbols',max=500)])





from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a text file',
        help_text='Each file should start with 4 numbers separated by a whitespace, followed by lines of number'
    )

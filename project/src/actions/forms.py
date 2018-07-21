from tinymce.widgets import TinyMCE

from django import forms

from src.actions.models import Action, Contact


class ActionAdminForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={
        'cols': 200,
        'rows': 90,
        'width': '1000px',
    }))

    class Meta:
        model = Action
        fields = '__all__'


class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = field.label.upper()

    class Meta:
        model = Contact
        fields = '__all__'

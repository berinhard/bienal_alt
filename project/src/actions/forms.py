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
    accept_file_upload = forms.BooleanField(required=False, label='Autorizo o uso do arquivo enviado para ser usado exclusivamente nas ações do Outra 33ª Bienal de São Paulo. O projeto se compromete a não utilizar os arquivos para outros fins, que não o da pesquisa artística.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'accept_file_upload':
                continue
            field.label = field.label.upper()

    def clean(self):
        cleaned_data = super().clean()
        upload = cleaned_data.get('upload')
        accepted = cleaned_data.get('accept_file_upload')

        if upload and not accepted:
            raise forms.ValidationError('É necessário autorização para enviar o arquivo.')
        return cleaned_data

    class Meta:
        model = Contact
        fields = '__all__'

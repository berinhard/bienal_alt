import yaml
from tinymce.widgets import TinyMCE

from django import forms
from django.utils.translation import gettext as _

from src.actions.models import Action, Contact, AnalyzedImage


class ActionAdminForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={
        'cols': 200,
        'rows': 90,
        'width': '1000px',
    }))

    class Meta:
        model = Action
        fields = '__all__'


class AnalyzedImageAdminForm(forms.ModelForm):
    error_messages = {
        "info": _("Este campo precisa estar num formato YAML válido. Teste aqui http://www.yamllint.com/ para entender o erro e corrigí-lo.")
    }

    def clean_info(self):
        try:
            info = yaml.load(self.cleaned_data['info'])
            if not isinstance(info, dict):
                raise forms.ValidationError(self.error_messages['info'])

            msg = _("Está faltando o campo: {}")
            if 'analise' not in info:
                raise forms.ValidationError(msg.format('analise'))
            if 'produtos' not in info:
                raise forms.ValidationError(msg.format('produtos'))
            if 'categoria' not in info:
                raise forms.ValidationError(msg.format('categoria'))
        except (yaml.scanner.ScannerError, yaml.parser.ParserError):
            raise forms.ValidationError(self.error_messages['info'])
        return info

    class Meta:
        model = AnalyzedImage
        fields = '__all__'


class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = field.label.upper()

    class Meta:
        model = Contact
        fields = '__all__'

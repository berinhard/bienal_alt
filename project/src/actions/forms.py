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


default = {
    'analise': [],
    'produtos': [],
    'categoria': '',
    'thumbnails': []
}
default_yaml = yaml.dump(default)


class AnalyzedImageAdminForm(forms.ModelForm):
    error_messages = {
        "info": _("Este campo precisa estar num formato YAML válido. Teste aqui http://www.yamllint.com/ para entender o erro e corrigí-lo."),
        "info_en": _("Este campo precisa estar num formato YAML válido. Teste aqui http://www.yamllint.com/ para entender o erro e corrigí-lo."),
    }
    info = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 30,
        }),
        initial=default_yaml,
    )
    info_en = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 30,
        }),
        initial=default_yaml,
        label='Info (EN)'
    )

    def validate_yaml(self, field):
        try:
            info = yaml.load(self.cleaned_data[field])
            if not isinstance(info, dict):
                raise forms.ValidationError(self.error_messages[field])

            msg = _("Está faltando o campo: {}")
            if 'analise' not in info:
                raise forms.ValidationError(msg.format('analise'))
            if 'produtos' not in info:
                raise forms.ValidationError(msg.format('produtos'))
            if 'categoria' not in info and 'conteúdo' not in info:
                raise forms.ValidationError(msg.format('categoria'))
        except (yaml.scanner.ScannerError, yaml.parser.ParserError):
            raise forms.ValidationError(self.error_messages[field])
        return info

    def clean_info(self):
        return self.validate_yaml('info')

    def clean_info_en(self):
        return self.validate_yaml('info_en')

    class Meta:
        model = AnalyzedImage
        fields = '__all__'


class ContactForm(forms.ModelForm):
    accept_file_upload = forms.BooleanField(required=False, label=_('Autorizo o uso do arquivo enviado para ser usado exclusivamente nas ações do Outra 33ª Bienal de São Paulo. O projeto se compromete a não utilizar os arquivos para outros fins, que não o da pesquisa artística.'))

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
            raise forms.ValidationError(_('É necessário autorização para enviar o arquivo.'))
        return cleaned_data

    class Meta:
        model = Contact
        fields = '__all__'

from django.forms import ModelForm
from .models import Profiles

class ProfilForm(ModelForm):
    class Meta:
        model = Profiles
        fields = ['isim', 'resim']

    def __init__(self, *args, **kwargs):
        super(ProfilForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
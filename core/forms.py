from django import forms

from users.models import Ronin


class RoninForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['session'].widget = forms.HiddenInput()
        self.fields['session'].required = False

    class Meta:
        model = Ronin
        fields = ['session', 'address']

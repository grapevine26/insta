from django import forms
from .models import main
class mainForm(forms.ModelForm):
    class Meta:
        model = main
        fields = ('image', 'content', 'hashtag',)

    # def __init__(self, *args, **kwargs):
    #     super(mainForm, self).__init__(*args, **kwargs)
    #     self.fields['']
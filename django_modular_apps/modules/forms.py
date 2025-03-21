from django import forms
from crispy_forms.helper import FormHelper
from accounts.models import Module


class ModuleForm(forms.ModelForm):
    module_name = forms.CharField(
                        widget=forms.TextInput(
                        attrs={
                            'class':'form-control',
                            'aria-label':'Sizing example input',
                            'aria-describedby':'inputGroup-sizing',
                            'id':'ModuleName'
                            }),
                        label='')

    class Meta:
        model = Module
        fields = (
            'module_name',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True

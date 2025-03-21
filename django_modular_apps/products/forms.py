from django import forms
from accounts.models import Product
from crispy_forms.helper import FormHelper


class ProductForm(forms.ModelForm):
    name = forms.CharField(
                        widget=forms.TextInput(
                        attrs={
                            'class':'form-control',
                            'aria-label':'Sizing example input',
                            'aria-describedby':'inputGroup-name',
                            'id':'Name'
                            }),
                        label='Name')

    barcode = forms.CharField(
                        widget=forms.NumberInput(
                        attrs={
                            'class':'form-control',
                            'aria-label':'Sizing example input',
                            'aria-describedby':'inputGroup-barcode',
                            'id':'Barcode'
                            }),
                        label='Barcode')

    price = forms.CharField(
                        widget=forms.TextInput(
                        attrs={
                            'class':'form-control',
                            'aria-label':'Sizing example input',
                            'aria-describedby':'inputGroup-price',
                            'id':'Price',
                            }),
                        label='Price')

    stock = forms.IntegerField(
                        widget=forms.NumberInput(
                        attrs={
                            'class':'form-control',
                            'aria-label':'Sizing example input',
                            'aria-describedby':'inputGroup-stock',
                            'id':'Stock',
                            'min':'0'
                            }),
                        label='Stock')

    class Meta:
        model = Product
        fields =(
            'name',
            'barcode',
            'price',
            'stock'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True

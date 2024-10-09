from django import forms
from django.core.exceptions import ValidationError

from .models import Item, Category


class AddItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Category', empty_label='Category not selected',  widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Item
        fields = ['title', 'slug', 'price', 'discount', 'description', 'category', 'selling']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}),
            'selling': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': "checkbox"}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 255:
            raise ValidationError('Length exceeds 255 characters')

        return title


class OrderForm(forms.Form):
    ORDER_CHOICES = [
        ('field1', 'Field 1'),
        ('field2', 'Field 2'),
        ('field3', 'Field 3'),
    ]
    ordering = forms.ChoiceField(choices=ORDER_CHOICES, required=False)


class UploadFileForm(forms.Form):
    file = forms.FileField(label="File")
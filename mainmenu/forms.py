from django import forms
from .models import *
from django import forms
from .models import Collections

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collections
        fields = ['title', 'description', 'items', 'visibility']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter collection title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
            'items': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'visibility': forms.Select(attrs={'class': 'form-select'}),

from .models import Item, Tag

class ItemForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple,
        required=False
    )

    class Meta:
        model = Item
        fields = [
            'title',
            'status',
            'location',
            'description',
            'tags',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

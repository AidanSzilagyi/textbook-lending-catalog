from django import forms
from .models import Item, Tag, Collection

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


class CollectionForm(forms.ModelForm):
        class Meta:
            model = Collection
            fields = ['name', 'description', 'items', 'visibility']
            widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter collection title'}),
                'description': forms.Textarea(
                    attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
                'items': forms.SelectMultiple(attrs={'class': 'form-select'}),
                'visibility': forms.Select(attrs={'class': 'form-select'}),
            }
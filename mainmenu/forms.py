from django import forms
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

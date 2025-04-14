from django import forms
from .models import Item, Tag
from .models import Profile

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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # Ensure these fields exist in your Profile model (add them if needed)
        fields = ['profile_picture', 'description', 'interests', 'birthday']
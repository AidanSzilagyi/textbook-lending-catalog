from django import forms
from .models import Item, Tag, Collection, Profile

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ItemForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False
    )
    
    images = MultipleFileField(
        widget=MultipleFileInput(attrs={'class': 'form-control'}),
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
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
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
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'major', 'class_year', 'birthday']
        widgets = {
            'class_year': forms.Select(choices=Profile.CLASS_CHOICES),
        }

class ReviewForm(forms.Form):
    rating = forms.ChoiceField(
        choices=[(5, '5 Stars'), (4, '4 Stars'), (3, '3 Stars'), (2, '2 Stars'), (1, '1 Star')],
        widget=forms.RadioSelect,
        required=True
    )
    review_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False
    )

class ItemReviewForm(ReviewForm):
    pass

class UserReviewForm(ReviewForm):
    pass
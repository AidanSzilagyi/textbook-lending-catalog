from django import forms
from .models import Item, Tag, Collection, Profile
from django.utils import timezone

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

        def clean(self):
                cleaned_data = super().clean()
                selected_items = cleaned_data.get('items')
                visibility = cleaned_data.get('visibility')

                if visibility == 'private' and selected_items:
                    for item in selected_items:
                        # Check if this item exists in any *other* public collections
                        public_collections = item.collections_of.filter(visibility='public')
                        if public_collections.exists():
                            raise forms.ValidationError(
                                f"Item '{item.title}' is already in a public collection. "
                                f"Remove it from public collections before adding to a private one."
                            )
                return cleaned_data

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # Exclude items already in private collections
            private_items = Item.objects.filter(collections_of__visibility='private').distinct()

            # If editing an existing collection, allow its own items even if private
            instance = kwargs.get('instance')
            if instance:
                allowed_ids = instance.items.values_list('id', flat=True)
                self.fields['items'].queryset = Item.objects.exclude(id__in=private_items).union(
                    Item.objects.filter(id__in=allowed_ids))
            else:
                self.fields['items'].queryset = Item.objects.exclude(id__in=private_items)

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

class DueDateForm(forms.Form):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date().isoformat()}),
        required=True,
        help_text="Select when this item is due back"
    )

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        if due_date < timezone.now().date():
            raise forms.ValidationError("Due date cannot be in the past")
        return due_date
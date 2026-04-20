from django import forms
from .models import Dataset


class DatasetForm(forms.ModelForm):
    label_classes_input = forms.CharField(
        required=True,
        label='Label Classes (comma-separated)',
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. cat, dog, bird',
            'class': 'form-input',
            'id': 'id_label_classes_input',
        })
    )

    class Meta:
        model = Dataset
        fields = ['name', 'description', 'file_type', 'annotation_task', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Dataset Name', 'id': 'id_ds_name'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'id': 'id_ds_desc'}),
            'file_type': forms.Select(attrs={'class': 'form-input', 'id': 'id_ds_filetype'}),
            'annotation_task': forms.Select(attrs={'class': 'form-input', 'id': 'id_ds_annotation_task'}),
            'status': forms.Select(attrs={'class': 'form-input', 'id': 'id_ds_status'}),
        }

    def save(self, commit=True):
        dataset = super().save(commit=False)
        raw = self.cleaned_data.get('label_classes_input', '')
        dataset.label_classes = [x.strip() for x in raw.split(',') if x.strip()]
        if commit:
            dataset.save()
        return dataset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            existing = self.instance.get_label_classes()
            self.fields['label_classes_input'].initial = ', '.join(existing)


class DataItemTextForm(forms.Form):
    text_items = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 10,
                                     'placeholder': 'One text item per line...', 'id': 'id_text_items'}),
        label='Text Items (one per line)'
    )

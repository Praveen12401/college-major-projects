from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        label="Upload Image",
        widget=forms.ClearableFileInput(attrs={
            'id': 'imageInput',
            'class': 'custom-input'
        })
    )
    target_size = forms.IntegerField(
        label="Target Size (in KB)",
        widget=forms.NumberInput(attrs={
            'id': 'sizeInput',
            'class': 'custom-input',
            'placeholder': 'Enter size in KB'
        })
    )

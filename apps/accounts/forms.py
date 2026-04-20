from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-input', 'id': 'id_username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-input', 'id': 'id_password'})
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email address', 'class': 'form-input', 'id': 'id_email'})
    )
    role = forms.ChoiceField(
        choices=[('annotator', 'Annotator'), ('admin', 'Admin')],
        widget=forms.Select(attrs={'class': 'form-input', 'id': 'id_role'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-input', 'id': 'id_reg_username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Password', 'id': 'id_password1'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Confirm Password', 'id': 'id_password2'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.lower().endswith('@gmail.com'):
            raise forms.ValidationError('Registration is restricted to valid @gmail.com email addresses only.')
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'id': 'id_prof_username'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'id': 'id_prof_email'}),
            'bio': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'id': 'id_prof_bio'}),
            'avatar': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'id_prof_avatar'}),
        }

from django import forms
from django.core.exceptions import ValidationError
from .models import User, Issue

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        min_length=6
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = User
        fields = [
            'id_number', 'first_name', 'last_name', 'phone_number',
            'address', 'email', 'password', 'confirm_password'
        ]
        widgets = {
            'id_number': forms.TextInput(attrs={'placeholder': 'Enter your 13-digit ID number'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your 10-digit phone number'}),
            'address': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your address'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
        }

    def clean_id_number(self):
        id_number = self.cleaned_data.get('id_number')
        if not id_number.isdigit() or len(id_number) != 13:
            raise ValidationError("ID number must be exactly 13 digits.")
        if User.objects.filter(id_number=id_number).exists():
            raise ValidationError("This ID number is already registered.")
        return id_number

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone and (not phone.isdigit() or len(phone) != 10):
            raise ValidationError("Phone number must be exactly 10 digits.")
        return phone

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and not first_name.isalpha():
            raise ValidationError("First name should contain only letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and not last_name.isalpha():
            raise ValidationError("Last name should contain only letters.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        if password and confirm and password != confirm:
            raise ValidationError("Passwords do not match.")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your 10-digit phone number'}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter your address', 'rows': 3}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
        }


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['issue_type', 'description', 'image', 'latitude', 'longitude']
        widgets = {
            'issue_type': forms.Select(),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the issue in detail'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }


class PasswordResetRequestForm(forms.Form):
    id_number = forms.CharField(
        max_length=13,
        label='ID Number',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your 13-digit ID number'})
    )


class PasswordResetForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
        label='New Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}),
        label='Confirm Password'
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

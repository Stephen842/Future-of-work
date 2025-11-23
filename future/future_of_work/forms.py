from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, Waitlist, Future_Of_Work
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

User = get_user_model()

class OnboardingForm(forms.Form):
    name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    country = CountryField(blank_label="Select your country").formfield(
        widget=CountrySelectWidget(
            attrs={
                "class": "bg-accentgray/60 border border-accentgray rounded-lg px-4 py-2 text-offwhite font-inter focus:border-gold focus:ring-gold focus:outline-none transition",
            }
        )
    )
    password = forms.CharField(min_length=3, widget=forms.PasswordInput)
    password_confirm = forms.CharField(min_length=3, widget=forms.PasswordInput)
    pod = forms.CharField(max_length=64)
    goal = forms.CharField(max_length=255)
    referral_code = forms.CharField(max_length=32, required=False)
    referred_by = forms.CharField(max_length=32, required=False)
    wallet = forms.BooleanField(required=False)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with that email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        pw1 = cleaned.get('password')
        pw2 = cleaned.get('password_confirm')
        if pw1 and pw2 and pw1 != pw2:
            raise ValidationError("Passwords do not match.")
        return cleaned

class SigninForm(forms.Form):
    """
    Basic sign-in form.
    Accepts username or email as identifier.
    """
    identifier = forms.CharField(label="Email or Username")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_identifier(self):
        """Ensure identifier (username or email) is stored in lowercase."""
        identifier = self.cleaned_data.get('identifier')
        if identifier:
            return identifier.lower()  # Convert to lowercase for case insensitivity
        return identifier

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].required = False

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'pod', 'goal']


class  WaitlistForm(forms.ModelForm):
    class Meta:
        model = Waitlist
        fields = '__all__'

class FutureOfWorkForm(forms.ModelForm):
    class Meta:
        model = Future_Of_Work
        fields = '__all__'
        exclude = ['fee', 'gateway', 'status']
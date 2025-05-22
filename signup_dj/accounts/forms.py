from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import INDIAN_STATES, REGISTER_AS_CHOICES, CustomUser
from .models import Blog
import re

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required. Letters only.',
        widget=forms.TextInput(attrs={'pattern': '[A-Za-z]+', 'title': 'Letters only'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required. Letters only.',
        widget=forms.TextInput(attrs={'pattern': '[A-Za-z]+', 'title': 'Letters only'})
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Required. Must be a valid Gmail address.',
        widget=forms.EmailInput(attrs={'pattern': '.+@gmail\\.com$', 'title': 'Must end with @gmail.com'})
    )
    
    # 📍 New: Profile image field (optional, will be uploaded to ImgBB in view)
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )
    

    # Address fields
    house_no_name = forms.CharField(
        max_length=100,
        required=True,
        help_text='Required.',
        label="House No / Name"
    )
    area = forms.CharField(
        max_length=100,
        required=True,
        help_text='Required.',
        label="Area"
    )
    landmark = forms.CharField(
        max_length=100,
        required=False,
        label="Landmark"
    )
    pincode = forms.CharField(
        max_length=6,
        required=True,
        help_text='6-digit PIN code only.',
        widget=forms.TextInput(attrs={'pattern': '[0-9]{6}', 'title': '6-digit number only'})
    )
    city = forms.CharField(
        max_length=50,
        required=True,
        label="Town / City"
    )
    state = forms.ChoiceField(
        choices=INDIAN_STATES,
        required=True
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text="At least 8 characters, not entirely numeric, and not too common."
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before for verification.",
    )

    register_as = forms.ChoiceField(
        choices=REGISTER_AS_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = CustomUser
        fields = (
            'username', 'first_name', 'last_name', 'email', 'profile_image',  # <-- include here
            'house_no_name', 'area', 'landmark', 'pincode',
            'city', 'state', 'password1', 'password2', 'register_as'
        )
        widgets = {
            'register_as': forms.RadioSelect
        }

    # Custom validations
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError("Email must end with @gmail.com")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[A-Za-z]+$', first_name):
            raise forms.ValidationError("First name can only contain letters")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[A-Za-z]+$', last_name):
            raise forms.ValidationError("Last name can only contain letters")
        return last_name

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if not re.match(r'^\d{6}$', pincode):
            raise forms.ValidationError("Pincode must be a 6-digit number")
        return pincode


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )



class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'image', 'category', 'summary', 'content']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 2}),
            'content': forms.Textarea(attrs={'rows': 6}),
        }

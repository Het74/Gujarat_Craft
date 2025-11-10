from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Product, ProductImage, ProductVideo, Category


class UserRegistrationForm(UserCreationForm):
    """Registration form with role selection"""
    ROLE_CHOICES = [
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    ]
    
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    full_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}))
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, widget=forms.RadioSelect(attrs={'class': 'role-radio'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'phone_number', 'role', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.full_name = self.cleaned_data['full_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user


class ProductForm(forms.ModelForm):
    """Form for adding/editing products"""
    # Note: Multiple file upload is handled in the view using request.FILES.getlist('images')
    images = forms.ImageField(widget=forms.FileInput(attrs={'accept': 'image/*'}), required=False)
    video = forms.FileField(required=False, widget=forms.FileInput(attrs={'accept': 'video/*'}))
    video_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter video URL (optional)'}))

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'stock_status', 'category', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Enter product description'}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'placeholder': 'Enter price'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'stock_status': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class UserSettingsForm(forms.ModelForm):
    """Form for user settings"""
    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = CustomUser.ROLE_ARTIST
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    pass


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'bio', 'profile_photo',
            'city', 'state', 'website', 'soundcloud_url', 'spotify_url',
            'youtube_url', 'instagram_url', 'facebook_url', 'twitter_url',
            'portfolio_url',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

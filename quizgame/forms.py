from django import forms
from .models import CustomUser, Questions
from allauth.account.forms import LoginForm,SignupForm

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ' '}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': ' '}))

    class Meta:
        model = CustomUser
        fields = ['user_name', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'user_name': forms.TextInput(attrs={'placeholder': ' '}),
            'first_name': forms.TextInput(attrs={'placeholder': ' '}),
            'last_name': forms.TextInput(attrs={'placeholder': ' '}),
            'email': forms.EmailInput(attrs={'placeholder': ''}),
        }
        
class loginForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ' ', 'id': 'inputEmail'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={ 'placeholder': ' ', 'id': 'inputPassword'}))

class questionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['question', 'opt_a', 'opt_b', 'opt_c', 'opt_d', 'category', 'answer']
        
        widgets ={
            'question': forms.Textarea(attrs={'placeholder': ' '}),
            'opt_a': forms.TextInput(attrs={'placeholder': ' '}),
            'opt_b': forms.TextInput(attrs={'placeholder': ' '}),
            'opt_c': forms.TextInput(attrs={'placeholder': ' '}),
            'opt_d': forms.TextInput(attrs={'placeholder': ' '}),
            'category': forms.Select(attrs={'placeholder': ' '}, choices=Questions.CHOICES),
            'answer': forms.Select(attrs={'placeholder': ' ',}, choices=Questions.OPTIONS),
        }


class ChangePassForm(forms.Form):
    current_password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'tb'}))
    new_password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'tb'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'tb'}))


# class CustomSignUpForm(SignupForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['email'].label = 'Email or Username'

from django.shortcuts import get_object_or_404
from django import forms 
from .models import Ticket, Comment, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class TicketSubmissionForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Subject', 'id': 'floatingtitle'}), label="",)
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'floatingdescription','style': 'height: 200px;'}), label="")
    priority = forms.ChoiceField(
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],  # Define your priority choices here
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'floatingpriority',
            'placeholder': '',
        }),
        label="",
    )
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'floatingdescription',}), label="")
    class Meta:

        model = Ticket
        fields = [
            'title',
            'description',
            'priority',
            'image',
            
        ]
        

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email', 'id': 'floatingEmail'}), label='',)
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username', 'id': 'floatingUsername'}), label='',)
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'floatingPassword'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Re-Enter Password', 'id': 'floatingPassword'}), label='')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Username', 'id': 'floatingInput'}), label="",)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control ', 'placeholder': 'Enter Password', 'id': 'floatingPassword'}), label="")
    
class TicketUpdateForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'floatingtitle', 'readonly': 'readonly'}), label="",)
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'floatingdescription','style': 'height: 200px;', 'readonly': 'readonly'}), label="")
    priority = forms.ChoiceField(
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],  # Define your priority choices here
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'floatingpriority',
            'placeholder': '',
        }),
        label="",)
    status = forms.ChoiceField(
        choices=[('new', 'New'), ('in progress', 'In Progress'), ('resolved', 'Resolved')],  # Define your priority choices here
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'floatingpriority',
            'placeholder': '',
        }),
        label="",)
    assigned_to = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'floatingpriority',
            'placeholder': '',
        }),
        label="",)
    
    class Meta:
        model = Ticket
        fields = [
            'title',
            'description',
            'priority',
            'status',
            'assigned_to',
            
            
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate the choices for assigned_to with all users
        self.fields['assigned_to'].choices = [(user.id, user.username) for user in User.objects.all()]
    
    def clean_assigned_to(self):
        assigned_user_id = self.cleaned_data['assigned_to']
        user = get_object_or_404(User, id=assigned_user_id)
        return user

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'floatingcomment', 'style': 'height: 200px;'}), label="",
    )
    class Meta:
        model = Comment
        fields = [
            'comment',
        ]
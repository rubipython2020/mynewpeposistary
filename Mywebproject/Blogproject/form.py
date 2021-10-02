from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post,Profile,Comment

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        ]

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','body','status','restrict_comment']


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','body','status','restrict_comment']

#UserEditForm
#ProfileEditForm

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'placeholder':'Write Reply Here...',
                'rows':'4',
                'cols':'50'
            }
        )
    )
    class Meta:
        model = Comment
        fields = ('content',)
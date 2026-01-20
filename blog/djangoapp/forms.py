from django import forms

from .models import Post


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = ['title', 'content']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'test'}),
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'test'})
        }
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['name', 'text']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
#             'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a comment...'})
#         }
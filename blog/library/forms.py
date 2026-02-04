from django import forms

from .models import Loan, Student, Book, Author


class BorrowForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        empty_label='-- Select Student --',
        widget=forms.Select(attrs={'class': 'form-control'})

    )

    class Meta:
        model = Loan
        fields = ['student']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_year', 'cover', 'is_active', 'tags']
        # fields = '__all__'
        # exclude = ['is_active']

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'sheikvanet cignis dasaxeleba', 'autofocus': True}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'published_year': forms.NumberInput(attrs={'class': 'form', 'min': 1000,
                                                       'placeholder': "sheikvanet cignis gamochvebis tseli"}),
            'cover': forms.ClearableFileInput(
                attrs={'class': 'form-control', 'accept': 'image/*'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'tags': forms.CheckboxSelectMultiple(
                attrs={'class': 'form-check-input', }),

        }

        help_texts = {
            'title': 'sheikvanet cignis dasaxeleba',
            'cover': 'airchiet sasurveli garekani',
            'tags': 'airchiet tag',
        }
        labels = {
            'title': 'cignis saxeli',
            'cover': 'garekani',
            'tags': 'tag',
            'published_year': 'gamoshvebis celi',
            'is_active': 'aktiuria tu ara',
        }

    
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'birth_year']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'avtoris saxeli'}),
            'birth_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'dabadebis celi'})
        }

    labels = {
        'name': 'avtoris saxeli',
        'birth_year': 'dabadebis celi',
    }



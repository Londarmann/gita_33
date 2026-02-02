from django import forms

from .models import Loan, Student


class BorrowForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.all())

    class Meta:
        model = Loan
        fields = ['student']

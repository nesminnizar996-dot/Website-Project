# forms.py
from django import forms
from .models import Student

HOBBY_CHOICES = [
    ('Reading', 'Reading'),
    ('Sports', 'Sports'),
    ('Music', 'Music'),
    ('Travel', 'Travel'),
]

class StudentForm(forms.ModelForm):

    hobbies = forms.MultipleChoiceField(
        choices=HOBBY_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )

    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Student
        fields = '__all__'
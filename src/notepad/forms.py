from django import forms
from .models import Note

class NoteModelForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
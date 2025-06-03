from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Ваше имя'}),
            'email': forms.EmailInput(attrs={'class': 'input input-bordered w-full', 'placeholder': 'Ваш email'}),
            'phone': forms.TextInput(attrs={'class': 'input input-bordered w-full', 'placeholder': '+7 (___) ___-__-__'}),
            'subject': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'message': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 5, 'placeholder': 'Ваше сообщение'}),
        }

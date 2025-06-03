# from django import forms

# from .models import ServiceRequest

# class ServiceRequestForm(forms.ModelForm):
#     agree_terms = forms.BooleanField(
#         required=True,
#         label="Я согласен на обработку персональных данных"
#     )
    
#     class Meta:
#         model = ServiceRequest
#         fields = ['name', 'phone', 'car_model', 'service_date', 'service_type', 'comments']
#         widgets = {
#             'service_date': forms.DateInput(attrs={'type': 'date'}),
#             'comments': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Опишите проблему или укажите дополнительную информацию'}),
#         }
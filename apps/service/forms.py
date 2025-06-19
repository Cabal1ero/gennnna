from django import forms
from .models import ServiceRequest
from django.core.exceptions import ValidationError
from django.utils import timezone

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['name', 'phone', 'car_model', 'service_date', 'service_time', 'service_type', 'comments']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'tel',
                'required': True
            }),
            'car_model': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'required': True
            }),
            'service_date': forms.DateInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'date',
                'required': True,
                'min': timezone.now().date().isoformat()  # Минимальная дата - сегодня
            }),
            'service_time': forms.Select(attrs={
                'class': 'select select-bordered w-full',
                'required': True
            }),
            'service_type': forms.Select(attrs={
                'class': 'select select-bordered w-full',
                'required': True
            }),
            'comments': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full h-32',
                'placeholder': 'Опишите проблему или укажите дополнительную информацию'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Добавляем пустой выбор для времени
        self.fields['service_time'].choices = [('', 'Выберите время')] + list(ServiceRequest.TIME_SLOTS)
        
        # Добавляем пустой выбор для типа обслуживания
        self.fields['service_type'].choices = [('', 'Выберите тип обслуживания')] + list(ServiceRequest.SERVICE_TYPES)
    
    def clean_service_date(self):
        """Валидация даты"""
        service_date = self.cleaned_data.get('service_date')
        
        if service_date and service_date < timezone.now().date():
            raise ValidationError('Нельзя записаться на прошедшую дату')
        
        return service_date
    
    def clean(self):
        """Общая валидация формы"""
        cleaned_data = super().clean()
        service_date = cleaned_data.get('service_date')
        service_time = cleaned_data.get('service_time')
        
        if service_date and service_time:
            # Проверяем, не занято ли это время
            existing_requests = ServiceRequest.objects.filter(
                service_date=service_date,
                service_time=service_time,
                status='confirmed'
            )
            
            if existing_requests.exists():
                raise ValidationError(
                    f'Время {service_time} на {service_date.strftime("%d.%m.%Y")} уже занято. '
                    'Пожалуйста, выберите другое время.'
                )
        
        return cleaned_data

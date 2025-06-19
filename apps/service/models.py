from django.db import models
from apps.accounts.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, time

# Create your models here.

class ServiceRequest(models.Model):
    SERVICE_TYPES = [
        ('maintenance', 'Техническое обслуживание'),
        ('diagnostics', 'Диагностика'),
        ('engine_repair', 'Ремонт двигателя'),
        ('transmission_repair', 'Ремонт трансмиссии'),
        ('suspension_repair', 'Ремонт подвески'),
        ('brake_repair', 'Ремонт тормозной системы'),
        ('electrical_repair', 'Ремонт электрики'),
        ('other', 'Другое'),
    ]
    
    # Доступные временные слоты
    TIME_SLOTS = [
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
        ('18:00', '18:00'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    car_model = models.CharField(max_length=100, verbose_name="Марка и модель автомобиля")
    service_date = models.DateField(verbose_name="Предпочтительная дата")
    service_time = models.CharField(max_length=5, choices=TIME_SLOTS, verbose_name="Время записи")
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES, verbose_name="Тип обслуживания")
    comments = models.TextField(blank=True, null=True, verbose_name="Комментарии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заявки")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='service_app_requests', verbose_name="Пользователь")
    status = models.CharField(max_length=20, default='new', choices=[
        ('new', 'Новая'),
        ('confirmed', 'Подтверждена'),
        ('completed', 'Выполнена'),
        ('cancelled', 'Отменена'),
    ], verbose_name="Статус")
    
    def clean(self):
        """Валидация модели"""
        super().clean()
        
        # Проверяем, что дата не в прошлом
        if self.service_date and self.service_date < timezone.now().date():
            raise ValidationError({'service_date': 'Нельзя записаться на прошедшую дату'})
        
        # Проверяем занятость времени только для подтвержденных заявок
        if self.service_date and self.service_time:
            existing_requests = ServiceRequest.objects.filter(
                service_date=self.service_date,
                service_time=self.service_time,
                status='confirmed'
            )
            
            # Исключаем текущую заявку при редактировании
            if self.pk:
                existing_requests = existing_requests.exclude(pk=self.pk)
            
            if existing_requests.exists():
                raise ValidationError({
                    'service_time': f'Время {self.service_time} на {self.service_date.strftime("%d.%m.%Y")} уже занято'
                })
    
    def save(self, *args, **kwargs):
        """Переопределяем save для вызова clean"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    @classmethod
    def get_available_times(cls, date):
        """Возвращает доступные временные слоты для указанной даты"""
        if not date:
            return cls.TIME_SLOTS
        
        # Получаем занятые времена для подтвержденных заявок
        occupied_times = cls.objects.filter(
            service_date=date,
            status='confirmed'
        ).values_list('service_time', flat=True)
        
        # Возвращаем только свободные слоты
        available_slots = [
            (time_slot, time_display) 
            for time_slot, time_display in cls.TIME_SLOTS 
            if time_slot not in occupied_times
        ]
        
        return available_slots
    
    def __str__(self):
        return f"Заявка на сервис от {self.name} ({self.service_date} {self.service_time})"
    
    class Meta:
        verbose_name = "Заявка на сервис"
        verbose_name_plural = "Заявки на сервис"
        ordering = ['-created_at']
        # Добавляем уникальность для подтвержденных заявок
        constraints = [
            models.UniqueConstraint(
                fields=['service_date', 'service_time'],
                condition=models.Q(status='confirmed'),
                name='unique_confirmed_datetime'
            )
        ]

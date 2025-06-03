from django.db import models
from django.utils import timezone

class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('general', 'Общий вопрос'),
        ('sales', 'Покупка автомобиля'),
        ('service', 'Сервисное обслуживание'),
        ('test_drive', 'Запись на тест-драйв'),
        ('feedback', 'Отзыв о работе автосалона'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='general', verbose_name="Тема обращения")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_processed = models.BooleanField(default=False, verbose_name="Обработано")
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата обработки")
    processed_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='processed_messages',
        verbose_name="Кто обработал"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="Примечания")
    
    def mark_as_processed(self, user=None):
        """Отметить сообщение как обработанное"""
        self.is_processed = True
        self.processed_at = timezone.now()
        self.processed_by = user
        self.save()
    
    def __str__(self):
        return f"{self.name} - {self.get_subject_display()} ({self.created_at.strftime('%d.%m.%Y %H:%M')})"
    
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['-created_at']

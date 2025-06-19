from django.contrib import admin
from .models import CarOrder

@admin.register(CarOrder)
class CarOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'car', 'user', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'car__model__brand']
    search_fields = ['user__username', 'user__email', 'car__model__name', 'car__model__brand__name']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('car', 'user', 'status')
        }),
        ('Дополнительно', {
            'fields': ('comment', 'created_at')
        })
    )

from django.contrib import admin
from .models import ServiceRequest

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'car_model', 'service_date', 'service_time', 'service_type', 'status', 'created_at']
    list_filter = ['status', 'service_type', 'service_date', 'created_at']
    search_fields = ['name', 'phone', 'car_model']
    list_editable = ['status']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('name', 'phone', 'user')
        }),
        ('Детали записи', {
            'fields': ('car_model', 'service_date', 'service_time', 'service_type')
        }),
        ('Дополнительная информация', {
            'fields': ('comments', 'status', 'created_at')
        })
    )
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        
        # Если заявка подтверждена, делаем дату и время только для чтения
        if obj and obj.status == 'confirmed':
            readonly_fields.extend(['service_date', 'service_time'])
        
        return readonly_fields
    
    actions = ['confirm_requests', 'cancel_requests']
    
    def confirm_requests(self, request, queryset):
        """Подтвердить выбранные заявки"""
        updated = 0
        conflicts = []
        
        for service_request in queryset.filter(status='new'):
            try:
                service_request.status = 'confirmed'
                service_request.save()
                updated += 1
            except Exception as e:
                conflicts.append(f"{service_request.name} ({service_request.service_date} {service_request.service_time})")
        
        if updated:
            self.message_user(request, f'Подтверждено заявок: {updated}')
        
        if conflicts:
            self.message_user(
                request, 
                f'Не удалось подтвердить заявки (конфликт времени): {", ".join(conflicts)}',
                level='WARNING'
            )
    
    confirm_requests.short_description = "Подтвердить выбранные заявки"
    
    def cancel_requests(self, request, queryset):
        """Отменить выбранные заявки"""
        updated = queryset.exclude(status__in=['completed', 'cancelled']).update(status='cancelled')
        self.message_user(request, f'Отменено заявок: {updated}')
    
    cancel_requests.short_description = "Отменить выбранные заявки"

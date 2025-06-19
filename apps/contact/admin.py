from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'created_at', 'is_processed']
    list_filter = ['subject', 'is_processed', 'created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

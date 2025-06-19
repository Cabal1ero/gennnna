from django.contrib import admin
from .models import CarBrand, CarModel, ModelImage, Equipment, EquipmentFeature, EquipmentImage, Car

@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    search_fields = ['name', 'country']
    prepopulated_fields = {'slug': ('name',)}

class ModelImageInline(admin.TabularInline):
    model = ModelImage
    extra = 1

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['brand', 'name', 'body_type', 'base_price', 'is_new', 'is_popular']
    list_filter = ['brand', 'body_type', 'fuel_type', 'transmission', 'is_new', 'is_popular']
    search_fields = ['name', 'brand__name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ModelImageInline]

class EquipmentFeatureInline(admin.TabularInline):
    model = EquipmentFeature
    extra = 1
    fields = ['name', 'category', 'is_included']

class EquipmentImageInline(admin.TabularInline):
    model = EquipmentImage
    extra = 1
    fields = ['image', 'title', 'order']

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['car_model', 'name', 'equipment_type', 'price']
    list_filter = ['equipment_type', 'car_model__brand']
    search_fields = ['name', 'car_model__name', 'car_model__brand__name']
    inlines = [EquipmentFeatureInline, EquipmentImageInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('car_model', 'name', 'equipment_type', 'price', 'description', 'main_image')
        }),
        ('Модификаторы характеристик', {
            'fields': ('power_modifier', 'max_speed_modifier', 'acceleration_modifier', 'fuel_consumption_modifier'),
            'classes': ('collapse',),
            'description': 'Модификаторы применяются к базовым характеристикам модели'
        }),
        ('Базовое оборудование', {
            'fields': (
                'has_climate_control', 'multimedia_system', 'seat_heating', 'has_heated_steering_wheel',
                'has_leather_seats', 'wheel_size'
            )
        }),
        ('Дополнительные опции', {
            'fields': (
                'has_sunroof', 'has_navigation', 'has_parking_sensors', 'has_rear_camera',
                'has_cruise_control', 'has_keyless_entry', 'has_auto_lights', 'has_rain_sensor'
            ),
            'classes': ('collapse',)
        })
    )

@admin.register(EquipmentFeature)
class EquipmentFeatureAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'name', 'category', 'is_included']
    list_filter = ['category', 'is_included', 'equipment__car_model__brand']
    search_fields = ['name', 'equipment__name']
    list_editable = ['is_included']

@admin.register(EquipmentImage)
class EquipmentImageAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'title', 'order']
    list_filter = ['equipment__car_model__brand']
    search_fields = ['title', 'equipment__name']
    list_editable = ['order']

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['model', 'equipment', 'year', 'color', 'price', 'is_available', 'is_new']
    list_filter = ['model__brand', 'year', 'fuel_type', 'transmission', 'is_available', 'is_new']
    search_fields = ['model__name', 'model__brand__name', 'color', 'vin']
    list_editable = ['is_available', 'is_new']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('model', 'equipment', 'year', 'color', 'price', 'image')
        }),
        ('Технические характеристики', {
            'fields': ('engine_volume', 'power', 'transmission', 'fuel_type', 'body_type', 'mileage')
        }),
        ('Дополнительная информация', {
            'fields': ('vin', 'description', 'equipment_display', 'is_available', 'is_new'),
            'classes': ('collapse',)
        })
    )

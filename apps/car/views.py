import json
from django.shortcuts import render, get_object_or_404
from .models import Car, CarModel, Equipment, EquipmentFeature, EquipmentImage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Min, Max

def services(request):
    cars_list = Car.objects.all()
    years = Car.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    # Apply filters
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    
    if year_from:
        cars_list = cars_list.filter(year__gte=year_from)
    if year_to:
        cars_list = cars_list.filter(year__lte=year_to)
    
    equipment = request.GET.get('equipment')
    if equipment:
        cars_list = cars_list.filter(equipment_display=equipment)
    
    body_types = request.GET.getlist('body_type')
    if body_types:
        cars_list = cars_list.filter(body_type__in=body_types)
    
    colors = request.GET.getlist('color')
    if colors:
        color_mapping = {
            'white': 'Белый',
            'black': 'Черный',
            'silver': 'Серебристый',
            'gray': 'Серый',
            'red': 'Красный',
            'blue': 'Синий',
            'green': 'Зеленый',
            'brown': 'Коричневый'
        }
        db_colors = [color_mapping.get(color, color) for color in colors if color in color_mapping]
        cars_list = cars_list.filter(color__in=db_colors)
    
    fuel_types = request.GET.getlist('fuel_type')
    if fuel_types:
        cars_list = cars_list.filter(fuel_type__in=fuel_types)
    
    transmissions = request.GET.getlist('transmission')
    if transmissions:
        cars_list = cars_list.filter(transmission__in=transmissions)
    
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    
    if price_from:
        cars_list = cars_list.filter(price__gte=price_from)
    if price_to:
        cars_list = cars_list.filter(price__lte=price_to)
    
    is_available = request.GET.get('is_available')
    if is_available == 'true':
        cars_list = cars_list.filter(is_available=True)
    
    is_new = request.GET.get('is_new')
    if is_new == 'true':
        cars_list = cars_list.filter(is_new=True)
    
    # Pagination
    paginator = Paginator(cars_list, 9)
    page = request.GET.get('page')
    
    try:
        cars = paginator.page(page)
    except PageNotAnInteger:
        cars = paginator.page(1)
    except EmptyPage:
        cars = paginator.page(paginator.num_pages)
    
    price_range = Car.objects.aggregate(min_price=Min('price'), max_price=Max('price'))
    
    context = {
        'cars': cars,
        'years': years,
        'price_range': price_range,
        'body_types': Car.BODY_TYPE_CHOICES,
        'equipment_types': Car.EQUIPMENT_CHOICES,
        'fuel_types': Car.FUEL_CHOICES,
        'transmission_types': Car.TRANSMISSION_CHOICES,
    }
    
    return render(request, 'services.html', context)


def car_detail(request, slug):
    car_model = get_object_or_404(CarModel, slug=slug)
    equipments = Equipment.objects.filter(car_model=car_model).prefetch_related('features', 'images')
    similar_models = CarModel.objects.filter(brand=car_model.brand).exclude(id=car_model.id)[:3]
    available_cars = Car.objects.filter(model=car_model, is_available=True)
    
    # Подготавливаем данные комплектаций для JavaScript
    equipments_data = []
    for equipment in equipments:
        # Группируем функции по категориям
        features_by_category = {}
        for feature in equipment.features.filter(is_included=True):
            if feature.category not in features_by_category:
                features_by_category[feature.category] = []
            features_by_category[feature.category].append(feature.name)
        
        # Получаем базовое оборудование
        base_equipment = equipment.get_base_equipment_dict()
        
        # Получаем рассчитанные технические характеристики
        specs = {
            'power': equipment.get_calculated_power(),
            'max_speed': equipment.get_calculated_max_speed(),
            'acceleration': equipment.get_calculated_acceleration(),
            'fuel_consumption': equipment.get_calculated_fuel_consumption()
        }
        
        # Получаем изображения для комплектации
        images = get_equipment_images(equipment, car_model)
        
        equipment_data = {
            'id': equipment.id,
            'name': equipment.name,
            'equipment_type': equipment.equipment_type,
            'price': str(equipment.price),
            'description': equipment.description or f'Комплектация {equipment.name} с расширенным набором опций',
            'features': features_by_category,
            'base_equipment': base_equipment,
            'specs': specs,
            'images': images
        }
        equipments_data.append(equipment_data)
    
    return render(request, 'car_detail.html', {
        'car_model': car_model,
        'equipments': equipments,
        'equipments_json': json.dumps(equipments_data),
        'similar_models': similar_models,
        'available_cars': available_cars,
    })


def get_equipment_images(equipment, car_model):
    """Получает изображения для комплектации"""
    images = {
        'main': '',
        'gallery': []
    }
    
    # Основное изображение
    if equipment.main_image:
        images['main'] = equipment.main_image.url
    elif car_model.image:
        images['main'] = car_model.image.url
    else:
        brand_name = car_model.brand.name.replace(' ', '+')
        model_name = car_model.name.replace(' ', '+')
        equipment_name = equipment.name.replace(' ', '+')
        images['main'] = f"https://placehold.co/800x600/blue/white?text={brand_name}+{model_name}+{equipment_name}"
    
    # Дополнительные изображения из галереи
    equipment_images = equipment.images.all().order_by('order')
    for eq_image in equipment_images:
        images['gallery'].append(eq_image.image.url)
    
    # Если нет дополнительных изображений, генерируем заглушки
    if not images['gallery']:
        brand_name = car_model.brand.name.replace(' ', '+')
        model_name = car_model.name.replace(' ', '+')
        equipment_name = equipment.name.replace(' ', '+')
        
        # Цвета в зависимости от типа комплектации
        color_schemes = {
            'standard': ['navy', 'teal', 'green', 'gray'],
            'comfort': ['violet', 'indigo', 'blue', 'cyan'],
            'luxury': ['orange', 'amber', 'yellow', 'lime'],
            'premium': ['rose', 'pink', 'red', 'orange'],
            'sport': ['slate', 'zinc', 'stone', 'neutral'],
        }
        
        colors = color_schemes.get(equipment.equipment_type, color_schemes['standard'])
        image_types = ['Night', 'Day', 'Side', 'Interior']
        
        for i, color in enumerate(colors):
            image_type = image_types[i] if i < len(image_types) else f'View{i+1}'
            images['gallery'].append(
                f"https://placehold.co/800x600/{color}/white?text={brand_name}+{model_name}+{equipment_name}+{image_type}"
            )
    
    return images

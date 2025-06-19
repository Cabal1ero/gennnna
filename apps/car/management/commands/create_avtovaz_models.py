from django.core.management.base import BaseCommand
from apps.car.models import CarBrand, CarModel, Equipment, EquipmentFeature
from decimal import Decimal

class Command(BaseCommand):
    help = 'Создает модели автомобилей АвтоВАЗа с комплектациями'

    def handle(self, *args, **options):
        self.stdout.write('Создание моделей АвтоВАЗа...')
        
        # Создаем марку LADA
        self.create_lada_brand()
        
        # Создаем модели
        self.create_lada_models()
        
        # Создаем комплектации
        self.create_equipments()
        
        # Создаем функции комплектаций
        self.create_equipment_features()
        
        self.stdout.write(self.style.SUCCESS('Модели АвтоВАЗа успешно созданы!'))

    def create_lada_brand(self):
        """Создание марки LADA"""
        brand, created = CarBrand.objects.get_or_create(
            name='LADA',
            defaults={
                'country': 'Россия',
                'description': 'АвтоВАЗ — российский автомобильный завод, крупнейший производитель легковых автомобилей в России.'
            }
        )
        if created:
            self.stdout.write(f'Создана марка: {brand.name}')
        return brand

    def create_lada_models(self):
        """Создание моделей LADA"""
        lada_brand = CarBrand.objects.get(name='LADA')
        
        models_data = [
            {
                'name': 'Vesta',
                'body_type': 'sedan',
                'base_price': Decimal('899000'),
                'engine_volume': Decimal('1.6'),
                'power': 106,
                'transmission': 'manual',
                'fuel_type': 'petrol',
                'fuel_consumption': Decimal('7.2'),
                'max_speed': 178,
                'acceleration': Decimal('10.9'),
                'length': 4410,
                'width': 1764,
                'height': 1497,
                'wheelbase': 2635,
                'clearance': 178,
                'trunk_volume': 480,
                'is_popular': True,
                'description': 'Современный седан с динамичным дизайном и передовыми технологиями.'
            },
            {
                'name': 'Granta',
                'body_type': 'sedan',
                'base_price': Decimal('649000'),
                'engine_volume': Decimal('1.6'),
                'power': 90,
                'transmission': 'manual',
                'fuel_type': 'petrol',
                'fuel_consumption': Decimal('7.0'),
                'max_speed': 167,
                'acceleration': Decimal('12.2'),
                'length': 4246,
                'width': 1700,
                'height': 1500,
                'wheelbase': 2476,
                'clearance': 160,
                'trunk_volume': 520,
                'is_popular': True,
                'description': 'Доступный и практичный седан для повседневного использования.'
            },
            {
                'name': 'XRAY',
                'body_type': 'crossover',
                'base_price': Decimal('799000'),
                'engine_volume': Decimal('1.6'),
                'power': 106,
                'transmission': 'manual',
                'fuel_type': 'petrol',
                'fuel_consumption': Decimal('7.1'),
                'max_speed': 176,
                'acceleration': Decimal('11.1'),
                'length': 4165,
                'width': 1764,
                'height': 1570,
                'wheelbase': 2592,
                'clearance': 195,
                'trunk_volume': 361,
                'is_new': True,
                'description': 'Стильный кроссовер с увеличенным дорожным просветом.'
            },
            {
                'name': 'Largus',
                'body_type': 'wagon',
                'base_price': Decimal('749000'),
                'engine_volume': Decimal('1.6'),
                'power': 90,
                'transmission': 'manual',
                'fuel_type': 'petrol',
                'fuel_consumption': Decimal('8.2'),
                'max_speed': 158,
                'acceleration': Decimal('13.5'),
                'length': 4470,
                'width': 1750,
                'height': 1636,
                'wheelbase': 2905,
                'clearance': 145,
                'trunk_volume': 560,
                'description': 'Просторный универсал для семьи и работы.'
            },
            {
                'name': 'Niva Travel',
                'body_type': 'suv',
                'base_price': Decimal('899000'),
                'engine_volume': Decimal('1.7'),
                'power': 83,
                'transmission': 'manual',
                'fuel_type': 'petrol',
                'fuel_consumption': Decimal('10.5'),
                'max_speed': 142,
                'acceleration': Decimal('17.0'),
                'length': 4084,
                'width': 1680,
                'height': 1652,
                'wheelbase': 2200,
                'clearance': 220,
                'trunk_volume': 320,
                'description': 'Легендарный внедорожник с постоянным полным приводом.'
            },
        ]
        
        for model_data in models_data:
            model_data['brand'] = lada_brand
            
            car_model, created = CarModel.objects.get_or_create(
                brand=lada_brand,
                name=model_data['name'],
                defaults=model_data
            )
            if created:
                self.stdout.write(f'Создана модель: {car_model}')

    def create_equipments(self):
        """Создание комплектаций для каждой модели"""
        equipment_configs = {
            'standard': {
                'name_suffix': 'Стандарт',
                'price_add': 0,
                'description': 'Базовая комплектация с необходимым набором опций'
            },
            'comfort': {
                'name_suffix': 'Комфорт',
                'price_add': 80000,
                'description': 'Расширенная комплектация с дополнительными опциями комфорта'
            },
            'luxury': {
                'name_suffix': 'Люкс',
                'price_add': 150000,
                'description': 'Топовая комплектация с максимальным набором опций'
            },
        }
        
        for car_model in CarModel.objects.filter(brand__name='LADA'):
            for eq_type, config in equipment_configs.items():
                equipment, created = Equipment.objects.get_or_create(
                    car_model=car_model,
                    equipment_type=eq_type,
                    defaults={
                        'name': f'{car_model.name} {config["name_suffix"]}',
                        'price': car_model.base_price + config['price_add'],
                        'description': config['description']
                    }
                )
                if created:
                    self.stdout.write(f'Создана комплектация: {equipment}')

    def create_equipment_features(self):
        """Создание функций для каждой комплектации"""
        features_by_type = {
            'standard': [
                ('Подушка безопасности водителя', 'safety'),
                ('ABS', 'safety'),
                ('Электроусилитель руля', 'comfort'),
                ('Электростеклоподъемники передние', 'comfort'),
                ('Центральный замок', 'safety'),
                ('Иммобилайзер', 'safety'),
                ('Регулировка сиденья водителя по высоте', 'comfort'),
                ('Бортовой компьютер', 'multimedia'),
            ],
            'comfort': [
                ('Подушка безопасности пассажира', 'safety'),
                ('Кондиционер', 'comfort'),
                ('Электростеклоподъемники задние', 'comfort'),
                ('Подогрев передних сидений', 'comfort'),
                ('Мультимедийная система EnjoY', 'multimedia'),
                ('Камера заднего вида', 'safety'),
                ('Парктроник задний', 'safety'),
                ('Противотуманные фары', 'exterior'),
                ('Легкосплавные диски R15', 'exterior'),
                ('Круиз-контроль', 'comfort'),
            ],
            'luxury': [
                ('Климат-контроль', 'comfort'),
                ('Подогрев руля', 'comfort'),
                ('Подогрев зеркал', 'comfort'),
                ('Датчик света', 'comfort'),
                ('Датчик дождя', 'comfort'),
                ('Легкосплавные диски R16', 'exterior'),
                ('Кожаная отделка руля', 'interior'),
                ('Электрорегулировка зеркал', 'comfort'),
                ('Система контроля давления в шинах', 'safety'),
                ('ESP (система стабилизации)', 'safety'),
                ('Подлокотник передний', 'comfort'),
                ('Боковые подушки безопасности', 'safety'),
            ]
        }
        
        for equipment in Equipment.objects.filter(car_model__brand__name='LADA'):
            # Добавляем базовые функции для всех комплектаций
            base_features = features_by_type['standard']
            
            # Добавляем специфичные функции для комплектации
            if equipment.equipment_type == 'comfort':
                features = base_features + features_by_type['comfort']
            elif equipment.equipment_type == 'luxury':
                features = base_features + features_by_type['comfort'] + features_by_type['luxury']
            else:
                features = base_features
            
            for feature_name, category in features:
                feature, created = EquipmentFeature.objects.get_or_create(
                    equipment=equipment,
                    name=feature_name,
                    defaults={'category': category}
                )
                if created:
                    self.stdout.write(f'Создана функция: {feature_name} для {equipment}')
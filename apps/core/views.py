from django.shortcuts import render
from apps.car.models import CarModel, CarBrand
# Create your views here.
def home(request):
    car_models = CarModel.objects.all()
    brands = CarBrand.objects.all()
    
    return render(request, 'home.html', {
        'car_models': car_models,
        'brands': brands,
    })

def about(request):
    return render(request, 'about.html')
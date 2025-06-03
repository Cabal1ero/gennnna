from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from apps.car.models import Car
from .models import CarOrder


@login_required
def order_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if not car.is_available:
        messages.error(request, "К сожалению, этот автомобиль уже недоступен для заказа.")
        return redirect('car:car_detail', car_id=car_id)
    
    order = CarOrder.objects.create(
        car=car,
        user=request.user,
        status='new'
    )
    
    messages.success(request, f"Ваш заказ на {car.model} успешно создан! Наш менеджер свяжется с вами в ближайшее время.")
    
    return redirect('accounts:profile')

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(CarOrder, id=order_id)
    
    if order.user != request.user:
        messages.error(request, 'У вас нет прав для отмены этого заказа.')
        return redirect('accounts:profile')
    
    if order.status not in ['new', 'processing']:
        messages.error(request, 'Этот заказ нельзя отменить, так как он уже обрабатывается или выполнен.')
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        order.status = 'cancelled'
        order.save()
        
        messages.success(request, f'Заказ №{order.id} успешно отменен.')
        
    return redirect('accounts:profile')


# Create your views here.

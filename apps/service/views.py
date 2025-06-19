from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import ServiceRequest
from .forms import ServiceRequestForm
import json

# Create your views here.

def service_center(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            try:
                service_request = form.save(commit=False)
                
                if request.user.is_authenticated:
                    service_request.user = request.user
                    
                service_request.save()
                messages.success(
                    request, 
                    f'Ваша заявка успешно отправлена на {service_request.service_date.strftime("%d.%m.%Y")} '
                    f'в {service_request.service_time}! Мы свяжемся с вами в ближайшее время.'
                )
                return redirect('service:service_center')
            except Exception as e:
                messages.error(request, f'Ошибка при создании заявки: {str(e)}')
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'name': f"{request.user.first_name} {request.user.last_name}".strip(),
                'phone': request.user.profile.phone if hasattr(request.user, 'profile') else '',
            }
        form = ServiceRequestForm(initial=initial_data)
    
    return render(request, 'service_center.html', {'form': form})

@require_http_methods(["GET"])
def get_available_times(request):
    """AJAX endpoint для получения доступных временных слотов"""
    date_str = request.GET.get('date')
    
    if not date_str:
        return JsonResponse({'error': 'Дата не указана'}, status=400)
    
    try:
        from datetime import datetime
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        available_times = ServiceRequest.get_available_times(date)
        
        return JsonResponse({
            'available_times': [
                {'value': time_slot, 'display': time_display}
                for time_slot, time_display in available_times
            ]
        })
    except ValueError:
        return JsonResponse({'error': 'Неверный формат даты'}, status=400)

@login_required
def cancel_service(request, service_id):
    """Отмена заявки на сервисное обслуживание"""
    service_request = get_object_or_404(ServiceRequest, id=service_id)
    
    if service_request.user != request.user:
        messages.error(request, 'У вас нет прав для отмены этой заявки.')
        return redirect('accounts:profile')
    
    if service_request.status not in ['new', 'confirmed']:
        messages.error(request, 'Эту заявку нельзя отменить, так как она уже в работе или выполнена.')
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        service_request.status = 'cancelled'
        service_request.save()
        
        messages.success(request, f'Заявка на сервисное обслуживание №{service_request.id} успешно отменена.')
        
    return redirect('accounts:profile')

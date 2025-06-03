from django.shortcuts import render
from django.http import JsonResponse
from .forms import ContactForm

# Create your views here.
def contact_modal(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Ваше сообщение успешно отправлено!'
            })
        else:
            errors = {field: error[0] for field, error in form.errors.items()}
            return JsonResponse({
                'success': False,
                'errors': errors
            })
    
    return JsonResponse({'success': False, 'message': 'Неверный запрос'}, status=400)

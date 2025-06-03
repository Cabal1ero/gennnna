# # Django imports
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth import login, authenticate, update_session_auth_hash
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.http import JsonResponse
# from django import forms

# from django.db.models import Min, Max

# # Local imports
# from apps.accounts.models import User
# from apps.accounts.models import UserProfile
# from .models import Car, CarBrand, CarModel, Equipment, ServiceRequest
# from .forms import ServiceRequestForm

# # ============= Forms =============
# class UserRegistrationForm(forms.ModelForm):
#     password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)
#     email = forms.EmailField(required=True)
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)
#     phone = forms.CharField(required=False)
#     avatar = forms.ImageField(required=False)
    
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email')
    
#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Пароли не совпадают")
#         return password2
    
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
        
#         if commit:
#             user.save()
            
#             # Создаем или обновляем профиль пользователя
#             profile, created = UserProfile.objects.get_or_create(user=user)
#             if self.cleaned_data.get('phone'):
#                 profile.phone = self.cleaned_data['phone']
#             if self.cleaned_data.get('avatar'):
#                 profile.avatar = self.cleaned_data['avatar']
#             profile.save()
            
#         return user

# # ============= Main Views =============







# # ============= Authentication =============
# def auth(request):
#     register_form = UserRegistrationForm()
#     login_form = AuthenticationForm()
    
#     if request.method == 'POST':
#         form_type = request.POST.get('form_type')
        
#         if form_type == 'register':
#             register_form = UserRegistrationForm(request.POST, request.FILES)
#             if register_form.is_valid():
#                 user = register_form.save()
#                 username = register_form.cleaned_data.get('username')
#                 password = register_form.cleaned_data.get('password1')
#                 user = authenticate(username=username, password=password)
#                 login(request, user)
#                 messages.success(request, f'Аккаунт создан успешно! Добро пожаловать, {user.first_name}!')
#                 return redirect('autosalon:home')
#         else:
#             login_form = AuthenticationForm(data=request.POST)
#             if login_form.is_valid():
#                 username = login_form.cleaned_data.get('username')
#                 password = login_form.cleaned_data.get('password')
#                 user = authenticate(username=username, password=password)
#                 if user is not None:
#                     login(request, user)
#                     messages.success(request, f'Добро пожаловать, {user.first_name if user.first_name else user.username}!')
#                     return redirect('autosalon:home')
    
#     return render(request, 'registration/auth.html', {
#         'register_form': register_form,
#         'login_form': login_form
#     })

# # ============= Contact Form =============

# # ============= User Profile =============
# @login_required
# def profile_dashboard(request):
#     service_requests = ServiceRequest.objects.filter(user=request.user)
#     orders = CarOrder.objects.filter(user=request.user)
    
#     context = {
#         'service_requests': service_requests,
#         'orders': orders,
#     }
    
#     return render(request, 'profile/dashboard.html', context)

# @login_required
# def profile_update(request):
#     if request.method == 'POST':
#         action = request.POST.get('action', 'update_profile')
        
#         if action == 'update_profile':
#             user = request.user
#             user.first_name = request.POST.get('first_name', '')
#             user.last_name = request.POST.get('last_name', '')
#             user.email = request.POST.get('email', '')
#             user.save()
            
#             profile = user.profile
#             profile.phone = request.POST.get('phone', '')
            
#             if 'avatar' in request.FILES:
#                 profile.avatar = request.FILES['avatar']
            
#             if request.POST.get('remove_avatar') == 'true':
#                 profile.avatar = None
                
#             profile.save()
            
#             messages.success(request, 'Профиль успешно обновлен!')
        
#         elif action == 'change_password':
#             old_password = request.POST.get('old_password', '')
#             new_password1 = request.POST.get('new_password1', '')
#             new_password2 = request.POST.get('new_password2', '')
            
#             if not request.user.check_password(old_password):
#                 messages.error(request, 'Неверный текущий пароль.')
#                 return redirect('autosalon:profile')
            
#             if new_password1 != new_password2:
#                 messages.error(request, 'Новые пароли не совпадают.')
#                 return redirect('autosalon:profile')
            
#             if len(new_password1) < 4:
#                 messages.error(request, 'Пароль должен содержать не менее 4 символов.')
#                 return redirect('autosalon:profile')
            
#             request.user.set_password(new_password1)
#             request.user.save()
            
#             update_session_auth_hash(request, request.user)
            
#             messages.success(request, 'Пароль успешно изменен!')
        
#         return redirect('autosalon:profile')
    
#     return redirect('autosalon:profile')

# # ============= Service Center =============
# def service_center(request):
#     if request.method == 'POST':
#         form = ServiceRequestForm(request.POST)
#         if form.is_valid():
#             service_request = form.save(commit=False)
            
#             if request.user.is_authenticated:
#                 service_request.user = request.user
                
#             service_request.save()
#             messages.success(request, 'Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.')
#             return redirect('autosalon:service_center')
#     else:
#         initial_data = {}
#         if request.user.is_authenticated:
#             initial_data = {
#                 'name': f"{request.user.first_name} {request.user.last_name}".strip(),
#                 'phone': request.user.profile.phone if hasattr(request.user, 'profile') else '',
#             }
#         form = ServiceRequestForm(initial=initial_data)
    
#     return render(request, 'service_center.html', {'form': form})

# # ============= Orders and Cancellations =============

# @login_required
# def cancel_service(request, service_id):
#     service_request = get_object_or_404(ServiceRequest, id=service_id)
    
#     if service_request.user != request.user:
#         messages.error(request, 'У вас нет прав для отмены этой заявки.')
#         return redirect('autosalon:profile')
    
#     if service_request.status not in ['new', 'confirmed']:
#         messages.error(request, 'Эту заявку нельзя отменить, так как она уже в работе или выполнена.')
#         return redirect('autosalon:profile')
    
#     if request.method == 'POST':
#         service_request.status = 'cancelled'
#         service_request.save()
        
#         messages.success(request, f'Заявка на сервисное обслуживание №{service_request.id} успешно отменена.')
        
#     return redirect('autosalon:profile')
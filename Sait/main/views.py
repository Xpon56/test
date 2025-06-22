from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterForm, OrderForm, FeedbackForm, OrderStatusForm
from .models import Order  

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('order_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if username == 'admin':
            user = authenticate(request, username=username, password=password)
            if user and user.is_superuser:
                login(request, user)
                return redirect('admin_panel')
            else:
                error = "Неверный логин или пароль администратора"
                return render(request, 'login.html', {'error': error})
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('order_list')
        else:
            error = "Неверный логин или пароль"
            return render(request, 'login.html', {'error': error})
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def order_list(request):
    orders = request.user.order_set.all()
    feedback_forms = [FeedbackForm(instance=order) for order in orders]
    
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        form = FeedbackForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    
    return render(request, 'order_list.html', {
        'orders': zip(orders, feedback_forms)
    })

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'order_create.html', {'form': form})

def is_admin(user):
    return user.username == 'admin'

@user_passes_test(is_admin)
def admin_panel(request):
    orders = Order.objects.all()
    status_forms = [OrderStatusForm(instance=order) for order in orders]
    
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    
    return render(request, 'admin_panel.html', {
        'orders': zip(orders, status_forms)
    })



def home_redirect(request):
    """Перенаправление на страницу входа"""
    return redirect('login')
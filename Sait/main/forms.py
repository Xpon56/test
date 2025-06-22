from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Order
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        validators=[RegexValidator(
            regex='^[А-Яа-яЁё\s]+$',
            message='Только кириллические символы'
        )]
    )
    phone = forms.CharField(
        validators=[RegexValidator(
            regex=r'^\+7\(\d{3}\)-\d{3}-\d{2}-\d{2}$',
            message='Формат: +7(XXX)-XXX-XX-XX'
        )]
    )
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'phone', 'email', 'password1', 'password2')


    def clean_username(self):
        username = self.cleaned_data['username']
        
        # Для обычных пользователей: проверка кириллицы и длины
        if username != 'admin':
            if not re.match(r'^[а-яА-ЯёЁ]+$', username):
                raise ValidationError('Логин должен содержать только кириллические символы')
            
            if len(username) < 6:
                raise ValidationError('Логин должен быть не менее 6 символов')
        
        return username
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы Bootstrap и плейсхолдеры
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field].label
            })

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['transport_date', 'weight', 'dimensions', 'from_address', 'to_address', 'cargo_type']
        widgets = {
            'transport_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['feedback']

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not re.match(r'^[а-яА-ЯёЁ]+$', username) and username != 'admin':
            raise ValueError('Логин должен содержать только кириллические символы')
        
        if len(username) < 6 and username != 'admin':
            raise ValueError('Логин должен быть не менее 6 символов')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=30, 
        unique=True,
        verbose_name='Логин'
    )
    full_name = models.CharField(
        max_length=100,
        verbose_name='ФИО',
        validators=[RegexValidator(
            regex='^[А-Яа-яЁё\s]+$',
            message='Только кириллические символы и пробелы'
        )]
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон',
        validators=[RegexValidator(
            regex=r'^\+7\(\d{3}\)-\d{3}-\d{2}-\d{2}$',
            message='Формат: +7(XXX)-XXX-XX-XX'
        )]
    )
    email = models.EmailField(unique=True, verbose_name='Email')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'phone', 'email']
    
    def __str__(self):
        return self.username
    
    def clean(self):
        if not self.is_staff and self.username != 'admin':
            if not re.match(r'^[а-яА-ЯёЁ]+$', self.username):
                raise ValidationError({'username': 'Логин должен содержать только кириллические символы'})
            
            if len(self.username) < 6:
                raise ValidationError({'username': 'Логин должен быть не менее 6 символов'})

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('cancelled', 'Отменена'),
    ]
    
    CARGO_TYPES = [
        ('large', 'Крупное'),
        ('perishable', 'Скоропортящееся'),
        ('refrigerated', 'Требуется рефрижератор'),
        ('animals', 'Животные'),
        ('liquid', 'Жидкость'),
        ('furniture', 'Мебель'),
        ('waste', 'Мусор'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    transport_date = models.DateTimeField(verbose_name='Дата и время перевозки')
    weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Вес груза')
    dimensions = models.CharField(max_length=100, verbose_name='Габариты')
    from_address = models.TextField(verbose_name='Адрес отправления')
    to_address = models.TextField(verbose_name='Адрес доставки')
    cargo_type = models.CharField(max_length=20, choices=CARGO_TYPES, verbose_name='Тип груза')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    feedback = models.TextField(blank=True, null=True, verbose_name='Отзыв')
    
    def __str__(self):
        return f'Заявка #{self.id}'
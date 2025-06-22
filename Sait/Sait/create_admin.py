import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sait.settings')
django.setup()

from main.models import CustomUser

def create_admin():
    if not CustomUser.objects.filter(username='admin').exists():
        admin = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='gruzovik2024',
            full_name='Администратор Системы',
            phone='+7(999)-999-99-99'
        )
        print("Администратор создан!")
        print(f"Логин: admin")
        print(f"Пароль: gruzovik2024")
    else:
        print("Пользователь admin уже существует")

if __name__ == '__main__':
    create_admin()
from django.shortcuts import render
from .models import Client, Car, Repair

def home(request):
    # Всі записи з кожної таблиці
    clients = Client.objects.all()
    cars = Car.objects.all()
    repairs = Repair.objects.all()

    # Передача даних до шаблону
    return render(request, 'home.html', {
        'project_name': 'Ford Workshop Management System',
        'student_info': 'Дударенко Нікіта Іванович, Група ІПЗ-21009б',
        'clients': clients,
        'cars': cars,
        'repairs': repairs
    })

FROM python:3.13

WORKDIR /app

# Копіюємо файл requirements.txt у контейнер
COPY requirements.txt .

# Встановлюємо всі залежності з requirements.txt
RUN pip install -r requirements.txt

# Копіюємо весь код проєкту в контейнер
COPY . .

# Встановлюємо команду за замовчуванням
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

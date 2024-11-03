import psycopg
from tabulate import tabulate

# Підключення до бази даних
conn = psycopg.connect(
    host="localhost",
    port="5432",
    dbname="workshop_db",
    user="postgres",
    password="123"
)
cursor = conn.cursor()

# Функція для виведення таблиць та даних
def show_table_structure_and_data(table_name):
    table_name  = table_name.lower()
    # Структура таблиці
    cursor.execute(f"""
        SELECT column_name, data_type, character_maximum_length
        FROM information_schema.columns
        WHERE table_name = '{table_name}';
    """)
    structure = cursor.fetchall()
    print(f"\nСтруктура таблиці '{table_name}':")
    print(tabulate(structure, headers=["Column", "Data Type", "Max Length"], tablefmt="grid"))

    # Дані таблиці
    cursor.execute(f"SELECT * FROM {table_name};")
    data = cursor.fetchall()
    if data:
        headers = [desc[0] for desc in cursor.description]
        print(f"\nДані таблиці '{table_name}':")
        print(tabulate(data, headers=headers, tablefmt="grid"))
    else:
        print(f"\nТаблиця '{table_name}' порожня.")

# Виведення всіх таблиць
tables = ["Clients", "Cars", "Repairs"]
for table in tables:
    show_table_structure_and_data(table)

# Функція для виведення результатів запиту
def show_query_result(query, description):
    cursor.execute(query)
    data = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    print(f"\n{description}:")
    print(tabulate(data, headers=headers, tablefmt="grid"))

# Запит 1: Інформація про всі гарантійні ремонти, сортування назв клієнтів за алфавітом
show_query_result("""
    SELECT c.company_name, r.*
    FROM Repairs r
    JOIN Cars car ON r.car_id = car.car_id
    JOIN Clients c ON car.client_id = c.client_id
    WHERE r.repair_type = 'гарантійний'
    ORDER BY c.company_name ASC;
""", "Інформація про гарантійні ремонти")

# Запит 2: Вартість ремонту та вартість з урахуванням знижки для кожного автомобіля
show_query_result("""
    SELECT r.repair_id, car.model, c.company_name,
           r.hours_needed * r.hourly_rate AS repair_cost,
           (r.hours_needed * r.hourly_rate) * (1 - r.discount / 100.0) AS discounted_cost
    FROM Repairs r
    JOIN Cars car ON r.car_id = car.car_id
    JOIN Clients c ON car.client_id = c.client_id;
""", "Вартість ремонту з урахуванням знижки для кожного авто")

# Запит 3: Відображення інформації по ремонту для всіх авто заданої марки
def show_repairs_by_model(model):
    cursor.execute("""
        SELECT r.*, car.model, c.company_name
        FROM Repairs r
        JOIN Cars car ON r.car_id = car.car_id
        JOIN Clients c ON car.client_id = c.client_id
        WHERE car.model = %s;
    """, (model,))
    repairs_by_model = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    print(f"\nІнформація по ремонту для авто марки '{model}':")
    print(tabulate(repairs_by_model, headers=headers, tablefmt="grid"))

# Показ ремонту по конкретній марці
show_repairs_by_model('fiesta')

# Запит 4: Загальна сума, яку сплатив кожен клієнт
show_query_result("""
    SELECT c.company_name,
           SUM(r.hours_needed * r.hourly_rate * (1 - r.discount / 100.0)) AS total_paid
    FROM Repairs r
    JOIN Cars car ON r.car_id = car.car_id
    JOIN Clients c ON car.client_id = c.client_id
    GROUP BY c.company_name;
""", "Загальна сума, яку сплатив кожен клієнт")

# Запит 5: Кількість кожного типу ремонтів для кожного клієнта
show_query_result("""
    SELECT c.company_name, r.repair_type, COUNT(*) AS repair_count
    FROM Repairs r
    JOIN Cars car ON r.car_id = car.car_id
    JOIN Clients c ON car.client_id = c.client_id
    GROUP BY c.company_name, r.repair_type
    ORDER BY c.company_name, r.repair_type;
""", "Кількість кожного типу ремонтів для кожного клієнта")

# Запит 6: Кількість ремонтів для кожної марки автомобіля
show_query_result("""
    SELECT car.model, COUNT(*) AS repair_count
    FROM Repairs r
    JOIN Cars car ON r.car_id = car.car_id
    GROUP BY car.model
    ORDER BY car.model;
""", "Кількість ремонтів для кожної марки автомобіля")

# Закриття з'єднання
cursor.close()
conn.close()
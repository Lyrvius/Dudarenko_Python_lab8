import psycopg

# Підключення до PostgreSQL
conn = psycopg.connect(
    host="localhost",
    port="5432",
    dbname="workshop_db",
    user="postgres",
    password="123"
)

cursor = conn.cursor()

# Створення таблиць
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Clients (
        client_id SERIAL PRIMARY KEY,
        company_name VARCHAR(100) NOT NULL,
        account_number VARCHAR(20) UNIQUE,
        phone VARCHAR(15),
        contact_person VARCHAR(50),
        address TEXT
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Cars (
        car_id SERIAL PRIMARY KEY,
        model VARCHAR(20) CHECK (model IN ('fiesta', 'focus', 'fusion', 'mondeo')),
        price NUMERIC(10, 2),
        client_id INT REFERENCES Clients(client_id) ON DELETE SET NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Repairs (
        repair_id SERIAL PRIMARY KEY,
        start_date DATE,
        car_id INT REFERENCES Cars(car_id) ON DELETE CASCADE,
        repair_type VARCHAR(20) CHECK (repair_type IN ('гарантійний', 'плановий', 'капітальний')),
        hourly_rate NUMERIC(6, 2),
        discount NUMERIC(3, 2) CHECK (discount >= 0 AND discount <= 10),
        hours_needed INT
    );
""")

# Підтвердження змін
conn.commit()

# Закриття курсора і з'єднання
cursor.close()
conn.close()
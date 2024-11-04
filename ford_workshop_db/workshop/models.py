from django.db import models

class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    contact_person = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = 'clients'


class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.model} (ID: {self.car_id})"

    class Meta:
        db_table = 'cars'


class Repair(models.Model):
    repair_id = models.AutoField(primary_key=True)
    start_date = models.DateField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    repair_type = models.CharField(
        max_length=50,
        choices=[("гарантійний", "Гарантійний"), ("плановий", "Плановий"), ("капітальний", "Капітальний")]
    )
    hourly_rate = models.DecimalField(max_digits=5, decimal_places=2)
    discount = models.DecimalField(max_digits=3, decimal_places=1)
    hours_needed = models.IntegerField()

    def __str__(self):
        return f"Repair {self.repair_id} for Car {self.car.model}"

    class Meta:
        db_table = 'repairs'
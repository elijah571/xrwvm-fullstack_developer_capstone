from django.db import models

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Dealer(models.Model):
    full_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    zip = models.CharField(max_length=10)
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name


class CarModel(models.Model):
    CAR_TYPE_CHOICES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Wagon', 'Wagon'),
    ]

    name = models.CharField(max_length=100)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)  # <-- FK fixed
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.car_make.name} - {self.name}"


class Review(models.Model):
    name = models.CharField(max_length=100)
    dealership = models.ForeignKey(Dealer, on_delete=models.CASCADE)  # FK to Dealer
    review = models.TextField()
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.IntegerField()
    sentiment = models.CharField(max_length=20)
    purchase_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

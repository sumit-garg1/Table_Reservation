from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Table(models.Model):
    name=models.CharField(max_length=50)
    capacity=models.IntegerField()

    def __str__(self):
        return f"{self.name} (capacity:{self.capacity})"
class Reservation(models.Model):
    STATUS_CHOICES=[
        ("pending","Pending"),
        ("Attendance","Attendance"),
        ("no attend","no attend"),
        ("Cancelled by Staff", "Cancelled by Staff"),
    ]
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.table.name}on{self.date}at{self.time}-{self.status}"
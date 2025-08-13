from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Table(models.Model):
    name=models.CharField(max_length=50)
    capacity=models.IntegerField()

    def __str__(self):
        return f"{self.name} (capacity:{self.capacity})"
class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()
    
    def __str__(self):
        return f"{self.table.name}on{self.date}at{self.time}"
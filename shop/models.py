from django.db import models

# Create your models here.
class Customer(models.Model):
    phone = models.CharField(max_length=10, unique=True)
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone

class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    points_earned = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.phone} - ₹{self.amount}"
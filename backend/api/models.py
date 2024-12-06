from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True)
    purchase_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    warranty_expiration = models.DateField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class UserPhoneNumber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)  # Ensure this field is large enough to store phone numbers

    def __str__(self):
        return self.phone_number
    
class NotificationPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    notify_when = models.CharField(
        max_length=20,
        choices=[
            ('immediate', 'Immediately'),
            ('six_months', '6 months out'),
            ('one_month', '1 month out'),
            ('one_week', '1 week out'),
            ('day_of', 'Day of expiry'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.item.name} - {self.notify_when}"
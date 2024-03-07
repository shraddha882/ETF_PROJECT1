from django.db import models
from django.contrib.auth.models import User
# Create your models here.
 


class RegisteredUser(models.Model):

    Subscription_choices = [
        ('Unsubscribed', 'Unsubscribed'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
      
    ]
    
    username  = models.CharField(max_length = 255,null = False, unique = True,default = 'username')
    name = models.CharField(max_length=255, null  = False)
    email = models.EmailField(primary_key=True, null  = False)
    date_of_birth = models.DateField( null  = False)
    phone_number = models.CharField(max_length=10, null  = False)  # Assuming a reasonable length for phone numbers
    password = models.CharField(max_length=255, null  = False)
    login_status = models.BooleanField(default = False)
    is_verified = models.BooleanField(default = False)
    token = models.CharField(max_length=150, null =True)
    sub_status = models.CharField(max_length =20, default='Unsubscribed',  choices=Subscription_choices)
    


    def __str__(self):
        return self.name
    
    
class Wallet(models.Model):
    user = models.OneToOneField(RegisteredUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=1000000.00)  # Initial balance of 10 lakhs
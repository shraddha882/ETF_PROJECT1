from django.db import models
from django.contrib.auth.models import User
# Create your models here.
 


class RegisteredUser(models.Model):


    username  = models.CharField(max_length = 255,null = False, unique = True,default = 'username')
    name = models.CharField(max_length=255, null  = False)
    email = models.EmailField(primary_key=True, null  = False)
    date_of_birth = models.DateField( null  = False)
    phone_number = models.CharField(max_length=10, null  = False)  # Assuming a reasonable length for phone numbers
    password = models.CharField(max_length=255, null  = False)
    login_status = models.BooleanField(default = False)
    is_verified = models.BooleanField(default = False)
    token = models.CharField(max_length=150, null =True)
    
    

    def __str__(self):
        return self.name
    
    
class Wallet(models.Model):
    
    Subscription_choices = [
        ('Unsubscribed', 'Unsubscribed'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Diamond', 'Diamond'),
      
    ]
    
    period_choices = [
        ('1 month', '1 month'),
        ('3 months', '3 months'),
        ('6 months', '6 months'),
        ('1 year', '1 year'),
      
    ]
    
    user = models.OneToOneField(RegisteredUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=1000000.00)  # Initial balance of 10 lakhs
    sub_status = models.CharField(max_length =20, default='Unsubscribed',  choices=Subscription_choices)
    period = models.CharField(max_length=10, default='1 month',  choices=period_choices)
    start_date = models.DateField(null  = True)
    end_date = models.DateField(null  = True)
    remaining_days = models.IntegerField(null = True)
    
    def __str__(self):
        return self.sub_status
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

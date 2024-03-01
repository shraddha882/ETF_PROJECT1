from django.db import models
from registeredUser.models import RegisteredUser
# # Base abstract model for ticker data
class NIFTYBEES_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")

class ITBEES_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")


class GOLDBEES_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")

    
class SILVERBEES_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")


class SBIETFIT_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")
    
class EGOLD_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")

class ABSLNN50ET_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")

class CPSEETF_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")

class MAFANG_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")

class MOVALUE_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")

class ICICIB22_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")
    
class NIFITETF_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")
    
class DSPITETF_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")
    
class PSUBNKIETF_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")

class COMMOIETF_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")
    
class ITIETF_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")

class AXISTECETF_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")

class TECH_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")

class KOTAKPSUBK_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")

class DSPQ50ETF_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")


class INFRABEES_NS(models.Model):
    date = models.DateField(primary_key=True, default = '-')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    volume = models.BigIntegerField(null = True, default = '-')
    dividends = models.FloatField(null = True, default = '-')
    stock_splits = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.date.strftime("%Y-%m-%d")


class AllETF(models.Model):
    ASSET_TYPE_CHOICES = [
        ('COMMODITIES', 'Commodities'),
        ('STOCKS', 'Stocks'),
      
    ]
    Etfnames = models.CharField(primary_key=True, max_length = 225)
    # Date = models.DateField(null = True)
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')
    asset_type = models.CharField(max_length =20,null = True,  choices=ASSET_TYPE_CHOICES)


    def __str__(self):
        
        return self.Etfnames
    
class UserBuyetf(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('BUY', 'BUY'),
        ('SELL', 'SELL'),
      
    ]
    Username = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE,null = True)
    Date_time = models.DateTimeField("Date and Time", auto_now=False, auto_now_add=True,null = True)
    Etf_purchased = models.ForeignKey(AllETF, on_delete=models.CASCADE,null = True)
    Quantity = models.FloatField(max_length = 20, null = True)
    Cost = models.FloatField(max_length = 20, null = True)
    Purchase_close_value = models.FloatField(null=True)
    trans_type = models.CharField(max_length =20,null = True,  choices=TRANSACTION_TYPE_CHOICES)

    def __str__(self):
        
        return self.Username


    


    
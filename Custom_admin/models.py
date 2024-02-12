from django.db import models

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

class AllETF(models.Model):
    Etfnames = models.CharField(max_length = 225, default = 'Name')
    Open = models.FloatField(null = True, default = '-')
    high = models.FloatField(null = True, default = '-')
    low = models.FloatField(null = True, default = '-')
    close = models.FloatField(null = True, default = '-')

    def __str__(self):
        # return self.date
        return self.Etfnames
    
from django.db import models
from django_countries.fields import CountryField

class TaxProduct(models.Model):
    tax_name = models.CharField(max_length=100, verbose_name="Nom de la taxe")
    
    def __str__(self):
        return f"{self.tax_name}"
    
class TaxUser(models.Model):
    tax_name = models.CharField(max_length=100, verbose_name="Nom de la taxe")
    
    def __str__(self):
        return f"{self.tax_name}"
    
class TaxMatrice(models.Model):
    tax_product = models.ForeignKey(TaxProduct, on_delete=models.CASCADE)
    tax_user = models.ForeignKey(TaxUser, on_delete=models.CASCADE)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Taux (%)" )
    tax_account = models.CharField(max_length=100, verbose_name="Compte de taxe")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    def __str__(self):
        return f"{self.tax_product} - {self.tax_user}"
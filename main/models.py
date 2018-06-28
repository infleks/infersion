from __future__ import unicode_literals
from datetime import datetime
from django.db import models
# Create your models here.

class UserInfo(models.Model):
    userEmail = models.EmailField()
    userPassword = models.CharField(max_length=100)
    userPermission = models.CharField(max_length=2)

    def __str__(self):
        return self.userEmail 

class CustomerInfo(models.Model):
    customerName = models.CharField(max_length=50)
    customerSituation = models.CharField(max_length=10)

    def __str__(self):
        return str(self.pk) + " - " + self.customerName + "(" + self.customerSituation + ")"

class ProductManagerHistory(models.Model):
    prodManName = models.CharField(max_length=50)
    prodManEmail = models.EmailField(null=True, blank=True)
    prodManPhoneNumber = models.IntegerField()
    whenIsProdManResponsible = models.DateField(default=datetime.now, blank=True)  
    customer = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.prodManName

class TechnicalManagerHistory(models.Model):
    techManName = models.CharField(max_length=50)
    techManEmail = models.EmailField(null=True, blank=True)
    whenIsTechManResponsible =models.DateField(default=datetime.now, blank=True)
    techManPhoneNumber = models.IntegerField()
    customer = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.techManName

class ProductInfo(models.Model):
    productName = models.CharField(max_length=50)
    
    def __str__(self):
        return self.productName

class ProductModule(models.Model):
    moduleName = models.CharField(max_length=50)
    product = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.moduleName

class ProductVersion(models.Model):
    productVersionName = models.CharField(max_length=50)
    productmodule = models.ForeignKey(ProductModule, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.productVersionName

class DatabaseInfo(models.Model):
    databaseName = models.CharField(max_length=50)
    
    def __str__(self):
        return self.databaseName

class DatabaseVersion(models.Model):
    databaseVersionName = models.CharField(max_length=50)
    database = models.ForeignKey(DatabaseInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.databaseVersionName        

class ServerInfo(models.Model):
    serverName = models.CharField(max_length=50)
    
    def __str__(self):
        return self.serverName

class ServerVersion(models.Model):
    serverVersionName = models.CharField(max_length=50)   
    server = models.ForeignKey(ServerInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.serverVersionName

class ProductHistory(models.Model):
    prodInstallationTime  = models.DateTimeField(default=datetime.now, blank=True)
    url = models.CharField(max_length=100)
    url_database = models.CharField(max_length=100)
    productversion = models.ForeignKey(ProductVersion, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    databaseversion = models.ForeignKey(DatabaseVersion, on_delete=models.CASCADE)
    serverversion = models.ForeignKey(ServerVersion, on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.prodInstallationTimeAsString()

    def prodInstallationTimeAsString(self):
        return self.prodInstallationTime.strftime("%d-%m-%y %H:%M")

class TestProductHistory(models.Model):
    testInstallationTime  = models.DateTimeField(default=datetime.now, blank=True)
    url = models.CharField(max_length=100)
    url_database = models.CharField(max_length=100)
    productversion = models.ForeignKey(ProductVersion, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    databaseversion = models.ForeignKey(DatabaseVersion, on_delete=models.CASCADE)
    serverversion = models.ForeignKey(ServerVersion, on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.testInstallationTimeAsString()

    def testInstallationTimeAsString(self):
        return self.testInstallationTime.strftime("%d-%m-%y %H:%M")





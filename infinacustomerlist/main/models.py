from __future__ import unicode_literals
from datetime import datetime
from django.db import models
# Create your models here.

class CustomerInfo(models.Model):
    customerName = models.CharField(max_length=50)

    def __str__(self):
        return self.customerName

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
    prodInstallationTime  = models.DateField(default=datetime.now, blank=True)
    productversion = models.ForeignKey(ProductVersion, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    databaseversion = models.ForeignKey(DatabaseVersion, on_delete=models.CASCADE)
    serverversion = models.ForeignKey(ServerVersion, on_delete=models.CASCADE)

    def __str__(self):
        return self.prodInstallationTime

class TestProductHistory(models.Model):
    testInstallationTime  = models.DateField(default=datetime.now, blank=True)
    productversion = models.ForeignKey(ProductVersion, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE)
    databaseversion = models.ForeignKey(DatabaseVersion, on_delete=models.CASCADE)
    serverversion = models.ForeignKey(ServerVersion, on_delete=models.CASCADE)

    def __str__(self):
        return self.testInstallationTime

class InfinaWorkerHistory(models.Model):
    workerName = models.CharField(max_length=50)
    workerSurname = models.CharField(max_length=50)
    installationTime = models.DateField(default=datetime.now, blank=True)
    producthistory = models.ForeignKey(ProductHistory, on_delete=models.CASCADE, null=True, blank=True)
    testproducthistory = models.ForeignKey(TestProductHistory, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.workerName + " " + self.workerSurname 
'''
class User(models.Model):
    userName = models.CharField(max_length=50)
    userSurname = models.CharField(max_length=50)
    userPassword = models.CharField(max_length=100)

class UserPermission(models.Model):
    permissionNumber = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(ProductModule, on_delete=models.CASCADE)
'''
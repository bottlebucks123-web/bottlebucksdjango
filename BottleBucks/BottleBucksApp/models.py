from django.db import models

# Create your models here.
class LoginTable(models.Model):
    Username = models.CharField(max_length=30, null=True, blank=True)
    Password = models.CharField(max_length=30, null=True, blank=True)
    UserType = models.CharField(max_length=30, null=True, blank=True)

class   UserTable(models.Model):
    LOGINID = models.ForeignKey(LoginTable, on_delete=models.CASCADE)
    Name = models.CharField(max_length=30, null=True, blank=True)    
    Image = models.FileField(null=True, blank=True)    
    Address = models.CharField(max_length=300, null=True, blank=True)    
    Email = models.CharField(max_length=30, null=True, blank=True)    
    Phno = models.BigIntegerField(null=True, blank=True)    
    District = models.CharField(max_length=30, null=True, blank=True)    
    Pin = models.BigIntegerField(null=True, blank=True)
    point = models.IntegerField(null=True, blank=True)
    qr = models.ImageField(null=True, blank=True)

class RewardTable(models.Model):
    USERID = models.ForeignKey(UserTable,on_delete=models.CASCADE)
    Points = models.IntegerField(null=True, blank=True)
    Date = models.DateField(auto_now_add=True)

class GiftTable(models.Model):
    ProductName = models.CharField(max_length=30, null=True, blank=True)
    Description = models.CharField(max_length=300, null=True, blank=True)
    Quantity = models.IntegerField(null=True, blank=True, default=1)
    PointsEligible = models.IntegerField( null=True, blank=True)
    ProductImage = models.FileField( null=True, blank=True)

class AccountTable(models.Model):
    USERID= models.ForeignKey(UserTable,on_delete=models.CASCADE)
    Name=models.CharField(max_length=20,null=True,blank=True)
    ACno = models.BigIntegerField(null=True, blank=True)
    Bankname = models.CharField(max_length=20,null=True, blank=True)
    IFSCcode = models.CharField(max_length=30, null=True, blank=True)
    # Proof= models.FileField(null=True, blank=True)
    UPI= models.CharField(max_length=30, null=True, blank=True)
    
class NotificationTable(models.Model):
    
    USER_ID = models.ForeignKey(UserTable, on_delete=models.CASCADE, null=True, blank=True)
    Description= models.CharField(max_length=300, null=True, blank=True)

class BucksHistoryTable(models.Model):
    Date=models.DateField(auto_now_add=True)
    Time=models.TimeField(auto_now_add=True)
    Bucks=models.IntegerField(null=True,blank=True)

class RedeemHistory(models.Model):
    Date=models.DateField(auto_now_add=True)
    Time=models.TimeField(auto_now_add=True)
    Method=models.CharField(max_length=50,null=True,blank=True)
    Bucksused=models.IntegerField(null=True,blank=True)



class ClaimProduct(models.Model):
    USERID=models.ForeignKey(UserTable,on_delete=models.CASCADE,null=True,blank=True)
    PRODUCTID=models.ForeignKey(GiftTable,on_delete=models.CASCADE,null=True,blank=True)
    totalRewardSpend=models.IntegerField(null=True,blank=True)
    date=models.DateField(auto_now_add=True)
    Address=models.TextField(null=True, blank=True)

class ClaimPointAccount(models.Model):
    USERID = models.ForeignKey(UserTable, on_delete=models.CASCADE, null=True, blank=True)
    AccountId = models.ForeignKey(AccountTable, on_delete=models.CASCADE, null=True, blank=True)
    points = models.IntegerField(null=True, blank=True)        # store points redeemed
    redeemmoney = models.IntegerField(null=True, blank=True)   # store money value in ₹
    date = models.DateTimeField(auto_now_add=True)







    
    

    

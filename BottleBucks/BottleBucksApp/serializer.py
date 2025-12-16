from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from BottleBucksApp.models import *

class LoginSerializer(ModelSerializer):
    class Meta:
        model=LoginTable
        fields=['Username','Password','UserType']

class GiftSerializer(ModelSerializer):
    class Meta:
        model=GiftTable
        fields=['id','ProductName','Description','Quantity','PointsEligible','ProductImage']

class UserSerializer(ModelSerializer):
    class Meta:
        model=UserTable
        fields=['Name','Image','Address','Email','Phno','District','Pin']        

class ProfileSerializer(ModelSerializer):
    class Meta:
        model=UserTable
        fields=['Name','Image','Address','Email','Phno','District','Pin','qr','point']       

class RewardSerializer(ModelSerializer):
    class Meta:
        model=RewardTable
        fields=['USERID','Points']        
from rest_framework.serializers import ModelSerializer, SerializerMethodField

class AccountSerializer(ModelSerializer):

    class Meta:
        model = AccountTable
        fields = '__all__'
        read_only_fields = ['USERID']  



    

class NotificationSerializer(ModelSerializer):
    class Meta:
        model=NotificationTable
        fields=['Description']  

class BucksHistorySerializer(ModelSerializer):
    class Meta:
        model=BucksHistoryTable
        fields=['Date','Time','Bucks'] 

class RedeemHistorySerializer(ModelSerializer):
    class Meta:
        model=RedeemHistory
        fields=['Date','Time','Gift/method','Bucks used'] 


class ProfileAccountSer(ModelSerializer):
    user_name = serializers.CharField(source = 'USERID.Name')
    user_image = serializers.FileField(source = 'USERID.Image')
    user_point = serializers.IntegerField(source = 'USERID.point')
    user_address = serializers.CharField(source = 'USERID.Address')
    user_email = serializers.CharField(source = 'USERID.Email')
    user_qr = serializers.CharField(source = 'USERID.qr')
    class Meta:
        model = AccountTable
        fields = [ "id",'ACno', 'Bankname','Name', 'IFSCcode','UPI',"user_name",'user_image','user_point','user_address','user_email','user_qr']

class ClaimProductser(ModelSerializer):
    product_image=serializers.FileField(source='PRODUCTID.ProductImage')
    product_name=serializers.CharField(source='PRODUCTID.ProductName')
    class Meta:
        model=ClaimProduct
        fields=["USERID",'PRODUCTID','totalRewardSpend','date','product_image','product_name'] 

class ClaimPointAccountser(ModelSerializer):
    class Meta:
        model=ClaimPointAccount
        fields=["USERID",'AccountId','points','redeemmoney','date']

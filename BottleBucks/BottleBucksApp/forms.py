from django.forms import ModelForm
from BottleBucksApp.models import AccountTable, GiftTable, LoginTable, NotificationTable, RewardTable, UserTable

class Loginform(ModelForm):
    class Meta:
        model=LoginTable
        fields=['Username','Password','UserType']

class Giftform(ModelForm):
    class Meta:
        model=GiftTable
        fields=['ProductName','Description','Quantity','PointsEligible','ProductImage']

      
class Rewardform(ModelForm):
    class Meta:
        model=RewardTable
        fields=['USERID','Points']        

     

class Notificationform(ModelForm):
    class Meta:
        model=NotificationTable
        fields=['Description']  

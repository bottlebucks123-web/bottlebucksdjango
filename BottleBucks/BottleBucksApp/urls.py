
from django.contrib import admin
from django.urls import path

from BottleBucksApp.views import *

urlpatterns = [
    path('', LoginPage.as_view(), name='LoginPage'),
    path('RegisterPage',RegisterPage.as_view(),name='RegisterPage'),
    path('RewardsPage',RewardsPage.as_view(),name='RewardsPage'),    
    path('UsergiftPage',UsergiftPage.as_view(),name='UsergiftPage'),    
    path('UserPage',UserPage.as_view(),name='UserPage'),    
    path('home',HomePage.as_view(),name='HomePage'),   
    path('ApproveUser/<int:login_id>/',ApproveUser.as_view(),name='ApproveUser'),
    path('RejectUser/<int:login_id>/',RejectUser.as_view(),name='RejectUser'),
    path('ApprovedUsersPage',ApprovedUsersPage.as_view(),name='ApprovedUsers'),
    path('ViewgiftPage',ViewgiftPage.as_view(),name='Viewgift'),
    path('AddgiftPage',AddgiftPage.as_view(),name='Addgift'),
    path('DeleteProduct/<int:id>/',DeleteProduct.as_view(),name='DeleteProduct'),
    path('EditGift/<int:id>/',EditGift.as_view(),name='EditGift'),


    path('LoginAPI',LoginPageAPI.as_view()),
    path('UserAPI',UserReg_api.as_view()),
    path('ProductAPI',ProductAPI.as_view()),
    path('KycAPI/<int:id>',Kyc.as_view()),
    path('RedeemGiftAPI/<int:id>/<int:gift_id>',RedeemGift.as_view()),
    path('CreditPointsAPI/',CreditPointsAPIView.as_view()),
    path('profile/<int:id>',ProfileView.as_view()),
    path('BucksHistoryAPI',BucksHistoryAPI.as_view()),
    path('RedeemHistoryAPI/<int:id>',RedeemHistoryAPI.as_view()),
    path('ProfileViewAPI/<int:id>',ProfileViewAPI.as_view()),
    path('NotificationApi', NotificationApi.as_view()),
    path('UserNotificationApi/<int:id>', UserNotificationApi.as_view()),
    path('TransactionHistoryAPI/<int:id>',TransactionHistoryAPI.as_view()),
    path('scan-qr/', scan_qr_and_open_bin),
]

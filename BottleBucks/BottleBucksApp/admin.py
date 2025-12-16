from django.contrib import admin

from BottleBucksApp.models import *


# Register your models here.
admin.site.register(LoginTable)
admin.site.register(UserTable)
admin.site.register(RewardTable)
admin.site.register(GiftTable)
admin.site.register(AccountTable)
admin.site.register(NotificationTable)
admin.site.register(BucksHistoryTable)
admin.site.register(RedeemHistory)
admin.site.register(ClaimProduct)
admin.site.register(ClaimPointAccount)
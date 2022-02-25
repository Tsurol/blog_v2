from django.contrib import admin

from authentication import models

admin.site.register(models.AuthUser)
admin.site.register(models.UserProfile)
admin.site.register(models.UserAsset)
admin.site.register(models.UserCoinsRecord)
admin.site.register(models.LoginRecord)


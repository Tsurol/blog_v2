from django.contrib import admin
from blogsite import models

admin.site.register(models.Blog)
admin.site.register(models.Comment)
admin.site.register(models.Category)
admin.site.register(models.AdviceUpload)
admin.site.register(models.LoveRelated)
admin.site.register(models.Tag)

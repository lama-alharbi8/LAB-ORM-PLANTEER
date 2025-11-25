from django.contrib import admin
from .models import Plant,Comment,Country

# Register your models here.

class PlantAdmin(admin.ModelAdmin):
    list_display=('name','category','created_at','updated_at')
    list_filter = ('category',)

class CommentAdmin(admin.ModelAdmin):
    list_display=('user','plant','created_at')
    list_filter = ('plant',)

admin.site.register(Plant,PlantAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Country)
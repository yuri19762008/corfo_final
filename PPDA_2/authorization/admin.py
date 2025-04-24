from django.contrib import admin
from .models import ProfileType

# Register your models here.
@admin.register(ProfileType)
class ProfileTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'name')
    search_fields = ('name',)
    ordering = ('id',)
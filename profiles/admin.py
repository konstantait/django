from django.contrib import admin
from profiles.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'is_active')

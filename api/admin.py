from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Hobby, FriendRequest

class CustomUserAdmin(UserAdmin):
    # Display fields in the admin list view
    list_display = ('username', 'email', 'name', 'date_of_birth', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'name')
    ordering = ('username',)
    # Configure fieldsets for editing user details
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'date_of_birth', 'hobbies')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Hobby)
admin.site.register(FriendRequest)

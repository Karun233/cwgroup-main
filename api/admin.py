from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Hobby

# Register your models here.
class HobbyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  #
    search_fields = ('name',)  
admin.site.register(Hobby, HobbyAdmin)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'date_of_birth')  
    search_fields = ('username', 'email')  
    list_filter = ('date_of_birth',) 
    filter_horizontal = ('hobbies',) 
admin.site.register(CustomUser, CustomUserAdmin)
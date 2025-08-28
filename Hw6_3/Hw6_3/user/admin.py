from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Post


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','owner', 'created_at' )
    list_filter = ('created_at', 'owner')
    search_fields = ('title', 'content')


admin.site.register(CustomUser, CustomUserAdmin)

# Register your models here.

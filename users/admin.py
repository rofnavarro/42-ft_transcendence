from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class	CustomUserAdmin(UserAdmin):
	model = CustomUser
	list_display = ('email', 'username', 'nickname', 'is_staff', 'is_active', 'profile_picture')
	list_filter = ('is_staff', 'is_active')
	search_fields = ('email', 'username')
	ordering = ('email',)
	fieldsets = (
		(None, {'fields': ('email', 'username', 'nickname', 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'profile_picture')}),
		('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
		('Important dates', {'fields': ('last_login', 'date_joined', 'is_online')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
		),
	)

admin.site.register(CustomUser, CustomUserAdmin)

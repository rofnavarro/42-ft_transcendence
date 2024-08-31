from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class	CustomUserAdmin(UserAdmin):
	model = CustomUser
	list_display = ('email', 'username', 'is_staff', 'is_active')
	list_filter = ('is_staff', 'is_active')
	search_fields = ('email', 'username')
	ordering = ('email',)
	fieldsets = (
		(None, {'fields': ('email', 'username', 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name')}),
		('Permissions', {'fields': ('is_staff', 'is_active')}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
		),
	)

admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm
from authorization.utils import apply_permissions_based_on_profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'email', 'first_name', 'last_name', 'profile_type', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('profile_type', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('id',)

    readonly_fields = (
        'is_staff', 'is_superuser',
        'groups',
        'effective_permissions'  # 👈 Campo agregado
    )

    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'profile_type')}),
        ('Permisos', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups',
                'effective_permissions',  # 👈 Mostrado en admin
            )
        }),
        ('Fechas', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'profile_type', 'password1', 'password2'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.profile_type:
            apply_permissions_based_on_profile(obj)
        super().save_model(request, obj, form, change)

    @admin.display(description="Permisos Efectivos")
    def effective_permissions(self, obj):
        return ", ".join(sorted(obj.get_all_permissions()))
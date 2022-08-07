from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Follow


@admin.register(User)
class UserAppAdmin(UserAdmin):
    list_display = (
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'date_joined',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'first_name',
                    'last_name',
                    'email',
                    'password',
                )
            }
        ),
        (
            _('Permissions'), {
                'fields': (
                    'is_active',
                    'is_superuser',
                    'is_staff',
                    'groups',
                    'user_permissions',
                ),
            }
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            }
        ),
    )
    readonly_fields = (
        'last_login',
        'date_joined',
    )
    ordering = ('-date_joined',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'is_superuser',
                'is_staff',
                'is_active',
                'groups',
            ),
        }),
    )
    list_filter = (
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
    )
    list_editable = (
        'is_active',
        'is_staff',
        'is_superuser',
    )
    list_display_links = ('email',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'user',
        'following',
    )

    search_fields = (
        'user__username',
        'following__username',
    )

    list_filter = (
        'user__username',
        'following__username',
    )

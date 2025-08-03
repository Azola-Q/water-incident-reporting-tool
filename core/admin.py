from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe, format_html
from .models import User, Issue


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['id_number', 'first_name', 'last_name', 'email', 'phone_number', 'is_admin', 'is_active']
    list_filter = ['is_admin', 'is_active']
    fieldsets = (
        (None, {'fields': ('id_number', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id_number', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'password1', 'password2', 'is_admin'),
        }),
    )
    search_fields = ['id_number', 'first_name', 'last_name', 'email']
    ordering = ['id_number']
    filter_horizontal = ('groups', 'user_permissions')


class IssueAdmin(admin.ModelAdmin):
    list_display = [
        'get_issue_type_display',
        'user',
        'description_preview',
        'status',
        'status_badge',
        'severity_badge',
        'created_at',
        'image_preview',
        'location_display'
    ]
    list_filter = ['issue_type', 'status', 'severity', 'created_at']
    search_fields = ['issue_type', 'description', 'user__id_number', 'user__first_name', 'user__last_name']
    ordering = ['-created_at']
    list_editable = ['status']
    readonly_fields = ['image_preview']

    def get_issue_type_display(self, obj):
        return obj.get_issue_type_display()
    get_issue_type_display.short_description = 'Issue Type'

    def description_preview(self, obj):
        return (obj.description[:75] + '...') if len(obj.description) > 75 else obj.description
    description_preview.short_description = 'Description'

    def status_badge(self, obj):
        color_map = {
            'received': 'orange',
            'processing': 'blue',
            'completed': 'green',
        }
        color = color_map.get(obj.status, 'grey')
        return format_html(
            '<span style="color:white; background-color:{}; padding:3px 6px; border-radius:5px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def severity_badge(self, obj):
        color_map = {
            'low': 'gray',
            'moderate': 'blue',
            'high': 'orange',
            'critical': 'red',
        }
        color = color_map.get(obj.severity, 'black')
        return format_html(
            '<span style="color:white; background-color:{}; padding:3px 6px; border-radius:5px;">{}</span>',
            color,
            obj.get_severity_display()
        )
    severity_badge.short_description = 'Severity'

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="120" style="border-radius: 6px;" />')
        return "No image uploaded"
    image_preview.short_description = 'Evidence Image'

    def location_display(self, obj):
        try:
            lat = float(obj.latitude)
            lon = float(obj.longitude)
            if lat == 0 and lon == 0:
                return "Invalid location"
            return format_html(
            '<a href="https://maps.google.com/?q={},{}" target="_blank">📍 Lat: {:.5f}, Long: {:.5f}</a>',
            lat, lon, lat, lon
            )
        except (ValueError, TypeError):
            return "No location selected"
    location_display.short_description = 'Location'



admin.site.register(User, CustomUserAdmin)
admin.site.register(Issue, IssueAdmin)

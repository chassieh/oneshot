from django.contrib import admin
from .models import ProducerProfile


@admin.register(ProducerProfile)
class ProducerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'is_active', 'created_at']
    list_filter = ['is_active', 'genres']
    search_fields = ['user__username', 'user__email', 'company']
    filter_horizontal = ['genres']

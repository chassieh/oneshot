from django.contrib import admin
from .models import Genre, Submission, Payment


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['song_title', 'artist_name', 'genre', 'status', 'payment_completed', 'submitted_at']
    list_filter = ['status', 'genre', 'payment_completed']
    search_fields = ['song_title', 'artist_name', 'artist__email']
    readonly_fields = ['id', 'submitted_at', 'updated_at']
    list_editable = ['status']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'method', 'status', 'created_at']
    list_filter = ['method', 'status']
    search_fields = ['user__email', 'transaction_id']
    readonly_fields = ['id', 'created_at', 'updated_at']

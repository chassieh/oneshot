from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_ARTIST = 'artist'
    ROLE_PRODUCER = 'producer'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = [
        (ROLE_ARTIST, 'Artist'),
        (ROLE_PRODUCER, 'Producer'),
        (ROLE_ADMIN, 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_ARTIST)
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    website = models.URLField(blank=True)
    soundcloud_url = models.URLField(blank=True)
    spotify_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_artist(self):
        return self.role == self.ROLE_ARTIST

    def is_producer(self):
        return self.role == self.ROLE_PRODUCER

    def is_site_admin(self):
        return self.role == self.ROLE_ADMIN or self.is_staff

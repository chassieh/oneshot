from django.db import models
from django.conf import settings


class ProducerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='producer_profile')
    genres = models.ManyToManyField('submissions.Genre', related_name='producers')
    company = models.CharField(max_length=200, blank=True)
    credits = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='producers/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Producer: {self.user.get_full_name() or self.user.username}"

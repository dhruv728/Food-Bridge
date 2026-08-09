import uuid
from django.db import models
from common.gis import gis_models
from django.conf import settings

VERIFICATION_STATUS_CHOICES = (
    ('pending', 'Pending Verification'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
)

URGENCY_LEVEL_CHOICES = (
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('critical', 'Critical / Urgent'),
)

class NGOProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ngo_profile')
    organization_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='pending')
    verification_document_url = models.CharField(max_length=500, blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    capacity_per_day = models.IntegerField(default=100)
    address = models.TextField()
    location = gis_models.PointField(srid=4326, null=True, blank=True)
    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)

    # Notification preferences
    notify_email = models.BooleanField(default=True)
    notify_sms = models.BooleanField(default=True)
    notify_push = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organization_name} ({self.verification_status})"

class NGOFoodRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ngo = models.ForeignKey(NGOProfile, on_delete=models.CASCADE, related_name='food_requests')
    title = models.CharField(max_length=200)
    food_category = models.CharField(max_length=100)
    quantity_meals_needed = models.IntegerField()
    urgency_level = models.CharField(max_length=20, choices=URGENCY_LEVEL_CHOICES, default='medium')
    address = models.TextField()
    location = gis_models.PointField(srid=4326, null=True, blank=True)
    is_fulfilled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Request: {self.title} ({self.quantity_meals_needed} meals) by {self.ngo.organization_name}"

import uuid
from django.db import models
from common.gis import gis_models
from django.conf import settings

VEHICLE_TYPE_CHOICES = (
    ('on_foot', 'On Foot'),
    ('bike', 'Bicycle / Motorbike'),
    ('car', 'Car / Auto'),
    ('van', 'Delivery Van / Truck'),
)

class VolunteerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='volunteer_profile')
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, default='bike')
    is_available = models.BooleanField(default=True)
    current_location = gis_models.PointField(srid=4326, null=True, blank=True)
    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    total_deliveries = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Volunteer: {self.user.full_name} ({self.vehicle_type})"

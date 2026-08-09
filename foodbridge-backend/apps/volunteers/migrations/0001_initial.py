import uuid
from common.gis import gis_models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VolunteerProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('vehicle_type', models.CharField(choices=[('on_foot', 'On Foot'), ('bike', 'Bicycle / Motorbike'), ('car', 'Car / Auto'), ('van', 'Delivery Van / Truck')], default='bike', max_length=20)),
                ('is_available', models.BooleanField(default=True)),
                ('current_location', gis_models.PointField(blank=True, null=True, srid=4326)),
                ('rating_avg', models.DecimalField(decimal_places=2, default=5.0, max_digits=3)),
                ('total_deliveries', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='volunteer_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

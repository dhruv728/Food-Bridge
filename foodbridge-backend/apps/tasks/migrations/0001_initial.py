import uuid
from common.gis import gis_models
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('donations', '0001_initial'),
        ('volunteers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('assigned', 'Assigned'), ('picked_up', 'Picked Up'), ('in_transit', 'In Transit'), ('delivered', 'Delivered'), ('confirmed', 'Confirmed')], default='assigned', max_length=20)),
                ('pickup_time', models.DateTimeField(blank=True, null=True)),
                ('delivery_time', models.DateTimeField(blank=True, null=True)),
                ('proof_image_url', models.URLField(blank=True, max_length=500, null=True)),
                ('otp_code', models.CharField(blank=True, max_length=6, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('donation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='task', to='donations.donation')),
                ('volunteer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='volunteers.volunteerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='TaskLocationLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('location', gis_models.PointField(blank=True, null=True, srid=4326)),
                ('recorded_at', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_logs', to='tasks.task')),
            ],
            options={
                'ordering': ['-recorded_at'],
            },
        ),
    ]

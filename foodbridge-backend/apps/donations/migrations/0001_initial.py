import uuid
from common.gis import gis_models
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('donors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('food_type', models.CharField(max_length=100)),
                ('quantity_kg', models.DecimalField(decimal_places=2, max_digits=8)),
                ('estimated_meals', models.IntegerField()),
                ('perishability_window', models.DateTimeField()),
                ('pickup_address', models.TextField()),
                ('pickup_location', gis_models.PointField(blank=True, null=True, srid=4326)),
                ('status', models.CharField(choices=[('listed', 'Listed'), ('claimed', 'Claimed'), ('assigned', 'Assigned'), ('picked_up', 'Picked Up'), ('in_transit', 'In Transit'), ('delivered', 'Delivered'), ('confirmed', 'Confirmed'), ('closed', 'Closed'), ('cancelled', 'Cancelled'), ('expired', 'Expired')], default='listed', max_length=20)),
                ('images', models.JSONField(blank=True, default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='donors.donorprofile')),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['status', 'perishability_window'], name='donations_d_status_9f43a9_idx')],
            },
        ),
    ]

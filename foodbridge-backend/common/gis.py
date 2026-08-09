import logging
from django.db import models

logger = logging.getLogger(__name__)

try:
    from django.contrib.gis.db import models as gis_models
    from django.contrib.gis.geos import Point
    HAS_GIS = True
except (ImportError, Exception) as e:
    logger.warning(f"GDAL / GIS support not available in host environment: {e}. Falling back to non-GIS mode.")
    gis_models = models
    HAS_GIS = False

    if not hasattr(gis_models, 'PointField'):
        class DummyPointField(models.JSONField):
            def __init__(self, *args, **kwargs):
                kwargs.pop('srid', None)
                kwargs.pop('spatial_index', None)
                super().__init__(*args, **kwargs)

        gis_models.PointField = DummyPointField

    def Point(longitude, latitude, srid=4326):
        return {"longitude": float(longitude), "latitude": float(latitude), "srid": srid}

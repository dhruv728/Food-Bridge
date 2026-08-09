import sys
import types
import logging
from unittest.mock import MagicMock
from django.db import models

# Gracefully handle missing GDAL C-libraries on Windows host OS for pytest execution
try:
    import django.contrib.gis.gdal
except Exception:
    logging.warning("GDAL C-libraries not detected on host OS. Installing test runtime mock for django.contrib.gis.")
    
    class DummyPointField(models.JSONField):
        def __init__(self, *args, **kwargs):
            kwargs.pop('srid', None)
            kwargs.pop('spatial_index', None)
            super().__init__(*args, **kwargs)

    mock_gis_main = types.ModuleType('django.contrib.gis')
    mock_gis_db = types.ModuleType('django.contrib.gis.db')
    mock_gis_models = types.ModuleType('django.contrib.gis.db.models')
    mock_gis_fields = types.ModuleType('django.contrib.gis.db.models.fields')

    for attr in dir(models):
        setattr(mock_gis_models, attr, getattr(models, attr))
    mock_gis_models.PointField = DummyPointField
    mock_gis_fields.PointField = DummyPointField
    
    mock_gis_models.fields = mock_gis_fields
    mock_gis_db.models = mock_gis_models
    mock_gis_main.db = mock_gis_db

    mock_gdal = MagicMock()
    mock_gis_main.gdal = mock_gdal
    mock_gis_main.geos = MagicMock()

    sys.modules['django.contrib.gis'] = mock_gis_main
    sys.modules['django.contrib.gis.gdal'] = mock_gdal
    sys.modules['django.contrib.gis.geos'] = sys.modules['django.contrib.gis.main'] = mock_gis_main
    sys.modules['django.contrib.gis.db'] = mock_gis_db
    sys.modules['django.contrib.gis.db.models'] = mock_gis_models
    sys.modules['django.contrib.gis.db.models.fields'] = mock_gis_fields

    mock_gis_functions = types.ModuleType('django.contrib.gis.db.models.functions')
    mock_gis_functions.Distance = MagicMock()
    sys.modules['django.contrib.gis.db.models.functions'] = mock_gis_functions

    sys.modules['django.contrib.gis.forms'] = MagicMock()
    sys.modules['django.contrib.gis.forms.fields'] = MagicMock()

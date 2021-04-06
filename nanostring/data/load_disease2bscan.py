import os
from django.contrib.gis.utils import LayerMapping

from .models import Disease2BScanSegments


disease2bscansegments_data_path = os.path.join(
    os.getcwd(), 'data', 'spatialdata', 'disease2B_scan_segments_digitized.shp'
)

# Auto-generated `LayerMapping` dictionary for Disease2BScanSegments model
disease2bscansegments_mapping = {
    'dn': 'DN',
    'name': 'name',
    'geom': 'MULTIPOLYGON',
}


def run(verbose=True):
    layermap = LayerMapping(
        Disease2BScanSegments,
        disease2bscansegments_data_path,
        disease2bscansegments_mapping,
        transform=False #the shapeﬁle need to be converted to WGS84 (SRID=4326)
    )
    layermap.save(strict=True,verbose=verbose)
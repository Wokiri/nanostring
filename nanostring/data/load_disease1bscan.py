import os
from django.contrib.gis.utils import LayerMapping

from .models import Disease1BScanVector


disease1B_scan_AOI_digitized_gcs = os.path.join(
    os.getcwd(), 'data', 'spatialdata', 'disease1B_scan_AOI_digitized_gcs.shp'
)

# Auto-generated `LayerMapping` dictionary for Disease1BScanVector model
disease1bscanvector_mapping = {
    'fid': 'fid',
    'dn': 'DN',
    'name': 'name',
    'geom': 'MULTIPOLYGON',
}


def run(verbose=True):
    layermap = LayerMapping(
        Disease1BScanVector,
        disease1B_scan_AOI_digitized_gcs,
        disease1bscanvector_mapping,
        transform=False #the shapeﬁle needed is WGS84 (SRID=4326)
    )
    layermap.save(strict=True,verbose=verbose)
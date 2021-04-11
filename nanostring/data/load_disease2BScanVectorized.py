import os
from django.contrib.gis.utils import LayerMapping

from .models import Disease2BScanVectorized


disease2bscanvectorized_path = os.path.join(
    os.getcwd(), 'data', 'spatialdata', 'disease2B_scan_AOI_vectorized.shp'
)

# Auto-generated `LayerMapping` dictionary for Disease2BScanVectorized model
disease2bscanvectorized_mapping = {
    'fid': 'fid',
    'dn': 'DN',
    'name': 'name',
    'geom': 'MULTIPOLYGON',
}


def run(verbose=True):
    layermap = LayerMapping(
        Disease2BScanVectorized,
        disease2bscanvectorized_path,
        disease2bscanvectorized_mapping,
        transform=False #the shapeﬁle is already in WGS84 (SRID=4326)
    )
    layermap.save(strict=True,verbose=verbose)
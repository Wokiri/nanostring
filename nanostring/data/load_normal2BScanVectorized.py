import os
from django.contrib.gis.utils import LayerMapping

from .models import Normal2BScanVectorized


normal2bscanvectorized_path = os.path.join(
    os.getcwd(), 'data', 'spatialdata', 'normal2B_scan_AOI_vectorized.shp'
)

# Auto-generated `LayerMapping` dictionary for Normal2BScanVectorized model
normal2bscanvectorized_mapping = {
    'fid': 'fid',
    'dn': 'DN',
    'name': 'name',
    'geom': 'MULTIPOLYGON',
}


def run(verbose=True):
    layermap = LayerMapping(
        Normal2BScanVectorized,
        normal2bscanvectorized_path,
        normal2bscanvectorized_mapping,
        transform=False #the shapeﬁle is already in WGS84 (SRID=4326)
    )
    layermap.save(strict=True,verbose=verbose)
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
        transform=False #the shapeﬁle is in web_mercator and we'd wish it to remain as such
    )
    layermap.save(strict=True,verbose=verbose)
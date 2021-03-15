from rest_framework import serializers
from data.models import Cell_Types_for_Spatial_Decon

class Cell_Types_for_Spatial_Decon_Serializer(serializers .ModelSerializer):
    class Meta:
        model = Cell_Types_for_Spatial_Decon
        fields = [
            'cluster_id',
            'alias',
            'data_set',
            'number_of_cells',
            'cell_type1',
            'cell_type2',
            'cell_type3',
            'cell_type_specific',
            'cell_type_general',
            'cluster_name'
            ]
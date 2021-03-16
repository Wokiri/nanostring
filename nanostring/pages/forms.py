from django.contrib.gis import forms
from data.models import Cell_Types_for_Spatial_Decon

class UploadCellTypesForm(forms.Form):
    file = forms.FileField(
        label='Browse to Cell_Types_for_Spatial_Decon.csv file:'
        )

class SearchCellTypesForm(forms.Form):
    search_cell_type = forms.CharField(label='Search Cell Annotations', max_length=125, required=False,
    widget=forms.TextInput(
        attrs={'id':'myFIELD', 'class':'form-control mr-sm-1'}
        ))

class UpdateCellsTypeCSVsForm(forms.ModelForm):
    class Meta:
        model = Cell_Types_for_Spatial_Decon
        fields = '__all__'


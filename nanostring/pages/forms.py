from django.contrib.gis import forms

class UploadCellTypesForm(forms.Form):
    file = forms.FileField(label='Cell_Types_for_Spatial_Decon.csv file:')

class SearchCellTypesForm(forms.Form):
    search_cell_type = forms.CharField(label='Search Cell Type(s)', max_length=125, required=False,
    widget=forms.TextInput(
        attrs={'id':'myFIELD', 'class':'form-control mr-sm-1'}
        ))
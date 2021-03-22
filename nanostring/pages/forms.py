from django.contrib.gis import forms
from data.models import (
    Cell_Types_for_Spatial_Decon,
    Kidney_Sample_Annotations,
    Kidney_Feature_Annotation,
    )

class UploadCellTypesForm(forms.Form):
    file = forms.FileField(
        label='Browse to Cell_Types_for_Spatial_Decon.csv file:'
        )

class SearchSampleAnnotationsForm(forms.Form):
    search_value = forms.CharField(label='Search Kidney Sample Annotations', max_length=125, required=False,
    widget=forms.TextInput(
        attrs={'class':'form-control mr-sm-1'}
        ))

class SearchCellTypesForm(forms.Form):
    search_value = forms.CharField(label='Search Cell Annotations', max_length=125, required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control mr-sm-1'}
            )
        )

class SearchFeatureAnnotationsForm(forms.Form):
    search_value = forms.CharField(label='Search Kidney Feature Annotations', max_length=125, required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control mr-sm-1'}
            ))

class UpdateCellsTypeCSVsForm(forms.ModelForm):
    class Meta:
        model = Cell_Types_for_Spatial_Decon
        fields = '__all__'


class UpdateFeatureAnnotationForm(forms.ModelForm):
    class Meta:
        model = Kidney_Feature_Annotation
        fields = '__all__'


class UploadSampleAnnotationsForm(forms.Form):
    file = forms.FileField(
        label='Browse to Kidney_Sample_Annotations.csv file:'
        )


class UpdateSampleAnnotationsCSVForm(forms.ModelForm):
    class Meta:
        model = Kidney_Sample_Annotations
        fields = '__all__'

class UploadFeatureAnnotationsForm(forms.Form):
    file = forms.FileField(
        label='Browse to Kidney_Feature_Annotations.csv file:'
        )
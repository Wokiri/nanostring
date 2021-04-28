from django.contrib.gis import forms


class DownloadDataForm(forms.Form):
    DATA_NAMES = [
        ('Kidney_Sample_Annotations.txt', 'Kidney_Sample_Annotations.txt'),
        ('Kidney_Feature_Annotations.txt', 'Kidney_Feature_Annotations.txt'),
        ('Kidney_Raw_BioProbeCountMatrix.txt', 'Kidney_Raw_BioProbeCountMatrix.txt'),
        ('Kidney_Raw_TargetCountMatrix.txt', 'Kidney_Raw_TargetCountMatrix.txt'),
        ('Kidney_Q3Norm_TargetCountMatrix.txt', 'Kidney_Q3Norm_TargetCountMatrix.txt'),
        ('Cell_Types_for_Spatial_Decon.txt', 'Cell_Types_for_Spatial_Decon.txt'),
        ('Young_kidney_cell_profile_matrix.csv', 'Young_kidney_cell_profile_matrix.csv'),
        ('Kidney_ssGSEA.txt', 'Kidney_ssGSEA.txt'),
    ]

    data_name = forms.ChoiceField(
        label='Name of txt/csv file to download',
        required=False,
        choices=DATA_NAMES,
        widget=forms.Select(
            attrs={'class':'form-control mr-sm-1'}
            )
    
    )


from data.models import (
    Category,
    Cell_Types_for_Spatial_Decon,
    Kidney_Sample_Annotations,
    RawCSVFiles,
    Disease2BScanVectorized,
    Normal2BScanVectorized,
    )


class CategoryModelForm(forms.ModelForm):

    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control mr-sm-1',
                'cols':80,
                'rows':20
            }
        )
    )

    class Meta:
        model = Category
        fields = ['name', 'description']



class UploadCellTypesForm(forms.Form):
    file = forms.FileField(label='Browse to Cell_Types_for_Spatial_Decon.csv file:')


class SearchSampleAnnotationsForm(forms.Form):
    search_value = forms.CharField(
        label='Search Kidney Sample Annotations', max_length=125, required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control mr-sm-1'}
        )
    )

class SearchCellTypesForm(forms.Form):
    search_value = forms.CharField(label='Search Cell Annotations', max_length=125, required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control mr-sm-1'}
            )
        )


class UpdateCellsTypeCSVsForm(forms.ModelForm):
    class Meta:
        model = Cell_Types_for_Spatial_Decon
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

class UploadRawCSVFilesModelForm(forms.ModelForm):
    class Meta:
        model = RawCSVFiles
        fields = '__all__'




class SearchFeatureAnnotationsForm(forms.Form):
    search_value = forms.CharField(
        label='Search Feature Annotations (RTS_ID)',
        max_length=125,
        required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control mr-sm-1'}
            ))


class SearchProbeExpressionForm(forms.Form):
    search_value = forms.IntegerField(label='Search Probe Expression (ProbeName)', required=False,
        widget=forms.NumberInput(
            attrs={'class':'form-control mr-sm-1'}
            ))


class QuantileSearchForm(forms.Form):
    quantile_value = forms.DecimalField(
        label='Search Quantile Value',
        required=False,
        decimal_places=2,
        min_value=0,
        max_value =1,
        widget=forms.NumberInput(
            attrs={'class':'form-control mr-sm-1'}
            ))



class SearchTargetExpressionForm(forms.Form):
    search_value = forms.CharField(
        label='Search Target Expression (TargetName)',
        max_length=125,
        required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control mr-sm-1'}
            ))



class SearchNormalizedExpressionForm(forms.Form):
    search_value = forms.CharField(
        label='Search Normalized Expression (TargetName)',
        max_length=125,
        required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control mr-sm-1'}
            ))



class SearchKidneyssGSEAForm(forms.Form):
    search_value = forms.CharField(
        label='Search KidneyssGSEA',
        max_length=125,
        required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control mr-sm-1'}
            ))



class SearchAverageGeneExpressionForm(forms.Form):
    search_value = forms.CharField(
        label='Search AverageGeneExpression',
        max_length=125,
        required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control mr-sm-1'}
            ))


class Disease2BScanVectorizedModelForm(forms.ModelForm):

    name = forms.CharField(label='Update the NAME of Disease2BScanVectorized', max_length=254, required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control mr-sm-1'}
        ))

    class Meta:
        model = Disease2BScanVectorized
        fields = ['name']


class Normal2BScanVectorizedModelForm(forms.ModelForm):

    name = forms.CharField(label='Update the NAME of Normal2BScanVectorized', max_length=254, required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control mr-sm-1'}
        ))

    class Meta:
        model = Normal2BScanVectorized
        fields = ['name']


class ClusterPointsForm(forms.Form):
    number_of_clusters = forms.IntegerField(
        label='Number of Clusters to Plot',
        min_value=1,
        max_value =10,
        required=False,
        widget=forms.NumberInput(
            attrs={'class':'form-control mr-sm-1'}
            ))
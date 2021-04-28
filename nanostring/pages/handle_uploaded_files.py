from django.conf import settings
from pathlib import Path, PurePath
import pandas

from data.models import RawCSVFiles


all_raw_csv_files = RawCSVFiles.objects.all()


def sample_annotations_DF():
    if all_raw_csv_files.filter(file_name='Kidney_Sample_Annotations.csv'):
        file_name = PurePath(settings.MEDIA_ROOT, 'csv_uploads', 'Kidney_Sample_Annotations.csv')
        if Path(file_name).exists:
            return pandas.read_csv(
                file_name,
                header=0,
                delimiter=','
            )


def feature_annotations_DF():
    if all_raw_csv_files.filter(file_name='Kidney_Feature_Annotations.csv'):
        file_name = PurePath(settings.MEDIA_ROOT, 'csv_uploads', 'Kidney_Feature_Annotations.csv')
        if Path(file_name).exists:
            return pandas.read_csv(
                file_name,
                header=0,
                usecols=['RTS_ID', 'TargetName', 'ProbeID', 'Negative'],
                index_col='RTS_ID',
                delimiter=','
            )



def probe_expression_DF():
    if all_raw_csv_files.filter(file_name='Kidney_Raw_BioProbeCountMatrix.csv'):
        file_name = PurePath(settings.MEDIA_ROOT, 'csv_uploads', 'Kidney_Raw_BioProbeCountMatrix.csv')
        if Path(file_name).exists:
            return pandas.read_csv(
                file_name,
                header=0,
                index_col='ProbeName',
                usecols=lambda x: x != 'Unnamed: 0',
                delimiter=','
            )



def target_expression_DF():
    if all_raw_csv_files.filter(file_name='Kidney_Raw_TargetCountMatrix.csv'):
        file_name = PurePath(settings.MEDIA_ROOT, 'csv_uploads', 'Kidney_Raw_TargetCountMatrix.csv')
        if Path(file_name).exists:
            return pandas.read_csv(
                file_name,
                header=0,
                index_col='TargetName',
                usecols=lambda x: x != 'Unnamed: 0',
                delimiter=','
            )



def normalized_expression_DF():
    if all_raw_csv_files.filter(file_name='Kidney_Q3Norm_TargetCountMatrix.csv'):
        file_name = PurePath(settings.MEDIA_ROOT, 'csv_uploads', 'Kidney_Q3Norm_TargetCountMatrix.csv')
        if Path(file_name).exists:
            return pandas.read_csv(
                file_name,
                header=0,
                index_col='TargetName',
                usecols=lambda x: x != 'Unnamed: 0',
                delimiter=','
            )



def ssGSEA_expression_DF():
    if all_raw_csv_files.filter(file_name='Kidney_ssGSEA.csv'):
        file_name = PurePath(settings.MEDIA_ROOT, 'csv_uploads', 'Kidney_ssGSEA.csv')
        if Path(file_name).exists:
            return pandas.read_csv(
                file_name,
                header=0,
                index_col='Unnamed: 0.1',
                usecols=lambda x: x != 'Unnamed: 0',
                delimiter=','
            )



def average_gene_expression_DF():
    if all_raw_csv_files.filter(file_name='Young_kidney_cell_profile_matrix.csv'):
        file_name = PurePath(settings.MEDIA_ROOT, 'csv_uploads', 'Young_kidney_cell_profile_matrix.csv')
        if Path(file_name).exists:
            return pandas.read_csv(
                file_name,
                header=0,
                usecols=lambda x: x != 'Unnamed: 0',
                # usecols=lambda x: x == 0,
                delimiter=','
            )


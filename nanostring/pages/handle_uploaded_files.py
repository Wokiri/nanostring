from django.conf import settings
from pathlib import Path, PurePath
import pandas

from data.models import RawCSVFiles


all_raw_csv_files = RawCSVFiles.objects.all()


def feature_annotations_DF():
    if all_raw_csv_files.filter(file_name='KidneyFeatureAnnotations'):
        feature_annotations_file = PurePath(settings.MEDIA_ROOT, 'csv_uploads', 'Kidney_Feature_Annotations.csv')
        if Path(feature_annotations_file).exists:
            return pandas.read_csv(
                feature_annotations_file,
                header=0,
                usecols=['RTS_ID', 'TargetName', 'ProbeID', 'Negative'],
                index_col='RTS_ID',
                delimiter=','
            )



def probe_expression_DF():
    if all_raw_csv_files.filter(file_name='KidneyRawBioProbeCountMatrix'):
        probe_expression_file = PurePath(settings.MEDIA_ROOT, 'csv_uploads', 'Kidney_Raw_BioProbeCountMatrix.csv')
        if Path(probe_expression_file).exists:
            return pandas.read_csv(
                probe_expression_file,
                header=0,
                index_col='ProbeName',
                usecols=lambda x: x != 'Unnamed: 0',
                delimiter=','
            )


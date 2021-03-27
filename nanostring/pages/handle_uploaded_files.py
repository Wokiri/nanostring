from django.conf import settings
from pathlib import Path, PurePath
import pandas



def probe_expression_DF():
    probe_expression_file = PurePath(settings.MEDIA_ROOT, 'csv_uploads', 'Kidney_Raw_BioProbeCountMatrix.csv')
    if Path(probe_expression_file).exists:
        return pandas.read_csv(
            probe_expression_file,
            usecols=[i for i in range(1, 233)],
            index_col='ProbeName',
            delimiter=','
        )
# Generated by Django 3.1.4 on 2021-03-08 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cell_Types_for_Spatial_Decon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clusterID', models.CharField(blank=True, max_length=8, null=True)),
                ('alias', models.CharField(blank=True, max_length=8, null=True)),
                ('data_set', models.CharField(blank=True, max_length=250, null=True)),
                ('number_of_cells', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('cell_type1', models.CharField(blank=True, max_length=125, null=True)),
                ('cell_type2', models.CharField(blank=True, max_length=125, null=True)),
                ('cell_type3', models.CharField(blank=True, max_length=125, null=True)),
                ('cell_type_specific', models.CharField(blank=True, max_length=125, null=True)),
                ('cell_type_general', models.CharField(blank=True, max_length=125, null=True)),
                ('cluster_name', models.CharField(blank=True, max_length=125, null=True)),
            ],
            options={
                'ordering': ['clusterID', 'number_of_cells'],
            },
        ),
    ]

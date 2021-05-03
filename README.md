# <p align='center'>**[NANOSTRING SPATIAL OMICS HACKATHON](https://nanostring.devpost.com/?ref_content=followed_registered&ref_feature=follow&ref_medium=email&utm_campaign=followed_registered&utm_content=followed_user_registered_for_challenge&utm_medium=email&utm_source=transactional)**</p>

## <p>**Hackathon Results.**</p>

<br/>



<p align='center'><img src="https://dub01pap001files.storage.live.com/y4mfx3F1gQb46H0CDfeaKkBiifqPTH4PLVvjJb9K64mPM75KS5hTzQLXfLfHm8oXYz8iBZCiBAZVhtbZrIWoNtVIWam-F8xjo-l6MSl0dQDzeLNTWMRT0crbTeCM7zlH6f_gP0PjtoLri-rOpoysam8OcxPwV1eNLbD_Pk-Gk-JRXlUQow0eujek41h4PdKLaGN?width=1728&height=1152&cropmode=none" width="1728" alt="Main thumbnail"/></p>

&nbsp;&nbsp;<br/>

### Done & Prepared by: [@JWokiri](https://twitter.com/JWokiri). <br/>

---
<br/>

<h1 id='hackathon_overview'>Hackathon Overview</h1>

<br/>

### **Expectations**:
> "Creating a graphical representation of data through visual components such as maps, graphs, or other visual formats (e.g. tools that display trends or patterns).
You could create data analysis solutions that collect, interpret, and present data (e.g. tools that identify relationships or detect anomalies). Put your Machine Learning skills to good use and build solutions that use pre-trained models or train a model using the specific dataset." **Nanostring Spatial Omics**.

<br/>

### **What's Delivered**:
Using softwares `distributed under a permissive open source license`, I have developed a **web application** that
- reads raw data from CSVs files, and for each file,
- represents the data therein in appropriate formats, tabular or plots, depending on the contents of the file and the expected analysis output, or in ways suitable to present some useful information.

### These information might be relayed through:

- Maps: For data with spatial attributes
- Statistical Charts: For data with numerical records (e.g bar charts, pie charts, box plots...)
- Tabular summaries, e.g. descripription of a DataFrame, quantile tables, etc

## Screenshots of some of the outputs include:


### <p align='center'>Bar Graph showing Number of Cells against Cell clusterID</p>

<p align='center'><img src="https://dub01pap001files.storage.live.com/y4mh4x-COU_i6951EaEJvm7tepZRvfNCSEDAKBjiww3jIFb57vFVM7RMCVld2CY1tVyqv6KbdcBfacucXTGf-lUF64eHRZZUb_gbojiuAS8wJBw9Sj3EpcqMYJJ9mkcPxS-AsvV1o5CZycKU8-yT2pGEDWBba8qvajvcTdOpmifndku-QOykVWm8fLzATzkxNIt?width=1200&height=500&cropmode=none" width="1280" alt="Bar Graph showing Number of Cells against Cell clusterID"/></p>

### <p align='center'>Kidney sample annotations map with selected healthy cell</p>

<p align='center'><img src="https://dub01pap001files.storage.live.com/y4mmJOyrfR52BlOx9cMS4e_PKpBrqr_KGJofuJWrY73CNGM_VHopzMPuFeNHV-SxFoo4zq9ffk-YlxhvEjQnRhWq7iAa43ss3IK5phyggFMzn29lA92I_scNPT__xvHon0agwcXT8WdKD1IgotNnhDoCWqrt1v-Cmu3PoauzrBF8KdhdxGVMxRV9DE1rkPYDFiv?width=1280&height=800&cropmode=none" width="1280" alt="Kidney sample annotations map with selected healthy cell"/></p>

### <p align='center'>Screen shot with search value of neutrophil</p>

<p align='center'><img src="https://dub01pap001files.storage.live.com/y4mPh6qfRmKoQR7G0omjIMRBDpewKhCN_FniCRw24Jf8NTGAJxPZ6ah91CgMgG0VRAh3ijOIA6wFIxoB0JAzDlPvak2fQZkpAzEcA__itqhpvtOkTsSHF2ijE-nLzAEhQhIZvq-2Dc3W-6_Iritx033rFZ2HrXTxt1KsOtAWZfbzo8m42uZp04n2mscEnCUCzVC?width=1280&height=800&cropmode=none" width="1280" alt="Screen shot with search value of neutrophil"/></p>

### <p align='center'>Pie Chart showing Kidney Sample Annotations categorized by Disease Status</p>

<p align='center'><img src="https://dub01pap001files.storage.live.com/y4mu2k3Dxsqq7f-0ZlMdpKfmM25k35r63sOUyletrtF8ORdN3gJqGiGxWKdCuKlYp5JC0nWQQu4StlDndyCruV3Y5fs5_fTTPUW9i5TW0v2CnFgN0WiU0bsLM2Vt7aO6KZbUjkbNwhvw6FmIFMLZL0oCJi1OLfASROV5fB8fNVgK8EXC1dpfbU_9F-wzW68uyth?width=992&height=600&cropmode=none" width="992" alt="Pie Chart showing Kidney Sample Annotations categorized by Disease Status"/></p>

<br/><br/>

<h1 id='toc'>Table of Contents</h1>

<a href="#hackathon_overview">Hackathon Overview</a><br/>
<a href="#licences">Free & Open Source Softwares Used</a><br/><br/>


**<p>PROJECT IMPLEMENTATION**</p>
   
1. <a href="#env_setup">Environment Setup</a><br/>
2. <a href="#django_project">Django</a><br/>
3. <a href="#data_retrieval">Retrieving Data</a><br/>
4. <a href="#data_storage">Data storage into the database</a><br/>
5. <a href="#data_analysis">Data Analysis</a><br/>
6. <a href="#results_visualization">Results Visualization</a><br/>
7. <a href="#project_your_computer">This project in your computer</a><br/>

**<p>HACKATHON COMPLIANCE INFORMATION**</p>

8. <a href="#compliance_statement">Compliance Statement</a><br/>
9. <a href="#installation_procedure">Instalations & Procedure</a><br/>

  ---
<br/>

## <p id="env_setup">1. Environment Setup</p>

For a successful running of scripts in this project, and indeed a proper functioning of the the overall WebApp, it is highly recommended that all the packages listed in [requirements.txt](./requirements.txt) be installed.

At the core of these packages sits python which gives the 'base' platform upon which most of the others depend.

> **"The Python interpreter and the extensive standard library are freely available in source or binary form for all major platforms from the Python Web site, https://www.python.org/, and may be freely distributed."** Python Documentation.



Some of the reliant packages include:
Package            | Version
------------------- |---------
bokeh               |2.3.0
Django              |3.1.4
GDAL                |3.1.4
pandas              |1.2.3
psycopg2            |2.8.6
---------------------------


A detailed process of achieving these installations is covered <a href="#installation_procedure">here</a><br/>

<br/>

## <p id="django_project">2. Django Project</p>

Django is a python web framework designed to make common Web development tasks fast and easy. It is used to make database-driven Web apps. It is for these stated reasons, generally, that I thought to deliver this project using Django.

To highlight a few specifics:
- Django is built with (arguably) agreable design philosophies like:
  - Loose coupling
  - Less code
  - Don’t repeat yourself (DRY)
  - Explicit is better than implicit
  - Consistency
- Django runs on top of python which is in itself a simple to use, but real programming language, offering much more structure and support for large programs than shell scripts or batch files can offer.
- Being a very-high-level language, it has high-level data types built in, such as flexible arrays and dictionaries.

</br>

**With Django,** I have been able to perform all the data-science analyses depicted in this project. Once achieved and results obtained, whether they be tables or the various visual plots, django intergrates very well with pandas and bokeh to display these results in a screen.

<br/>

## <p id="data_retrieval">3. Retrieving Data</p>

The [python code (***data_retrieval.py***)](KidneyDataset/data_retrieval.py) which sits in the directory **KidneyDataset** plays the role of accessing the raw txt files from the appropriate [URL](http://nanostring-public-share.s3-website-us-west-2.amazonaws.com/GeoScriptHub/KidneyDataset/) *(given by Nanostring Spatial Omics)*, reading the contents of the text data, cleaning the data and writing both the txt file and a corresponding csv file into the same directory.

A much quicker and perhaps an more effective method of downloading the data may be achieved by visiting http://127.0.0.1:8000/download-data/ when the local server has been started. It functions more or less as the refered python code above (which indeed it is) only there is an added friendly user interface by using the [URL](http://127.0.0.1:8000/download-data/)


In so doing, it perfoms a few checks to minimize the possibilities of errors, i.e:
- Upon execution, the code requires one to input the text name with the extension suffix included (e.g ***Cell_Types_for_Spatial_Decon.txt***). The code will here asses that the name is okay in the sense that there are no spaces between characters and that it has a .txt extension. 
- If this validation is not passed, the appropriate error message(s) is (are) printed out.
- Should the naming be right, the code will attempt to download the data from the remote server and write both the text and csv for it. The assumption here is that the user will input an accurate file name as listed in this [URL](http://nanostring-public-share.s3-website-us-west-2.amazonaws.com/GeoScriptHub/KidneyDataset/).
- If during the running of the code a text file that is sort is found already existing in the present directory, a CSV file will be written from the contents of this txt file and no download would then be necessary.

<br/>


### <p align='center'>Image showing file explorer when data has been been downloaded & writen using the [data-download url](http://127.0.0.1:8000/download-data/)</p>

<p align='center'><img src="https://dub01pap001files.storage.live.com/y4mNVsDKmNgdK9sHC_q13TCRMa0GF-C27F4TP71BRlG45qUyJML8swaJOh7X4TLVwUl76q03kIToP9s6B1r10ktf_SMuIob3sPO7VVqpQFe9zMQymHBWybmfDygjas-ZfIOaKnNmfcMfOuxm02PdLYaO4o6_zqDJqqSQuB8oBrm0HWT-h8kFUXo1hbk1k8XifX8?width=1920&height=1080&cropmode=none" width="1920" alt="Downloading & writing data"/></p>

<br/>

## <p id="data_storage">4. Data storage into the database</p>

### CSV Data:

With django's Object Relational Mapper, the various csv files contents are uploaded into a database either as individual records or as whole files. The smaller files (whose scheema is easy to make)  have been fed and stored in the database as individual records hence making use django's rich Queryset API functionalities.

The larger csv files (with significantly large column records, hence a much more complex schema) are uploaded as a whole into a local storage but whose access is possible by django, and manipulation and interactions achieved through pandas.

<br/>

### Vector Spatial Data:

A sample of Disease2BScan image and Normal2BScan image have been digitized by identifying the portions that are highlighted as AOIs.

These digitized data which requires a database with geometry support, hence use of PostGIS, have been both stored into the database and reading made possible by use of openlayers javascript library. Openlayers is a free and open source platform that makes it possible to view spatial data and interact with them in a number of useful supported ways.

<br/>



## <p id="data_reading">5. Reading stored data</p>

Most of the data stored into the database will at some point be read for statistical analysis or display purposes. As such the pandas package is heavily depended on to read these data. Pandas is a feature-rich package that provides a great deal of data reading options including **`read_sql_query`** and **`read_csv`** both of which, depending on the situation, have been employed in the handling of this project, e.g...

```python
from django.conf import settings
from pathlib import Path, PurePath
from django.db import connection
import pandas



# read_sql_query
cells_type_data = pandas.read_sql_query('''
    SELECT * FROM data_cell_types_for_spatial_decon
    ''',
    connection)


# OR


# read_csv
def probe_expression_DF():
    probe_expression_file = PurePath(settings.MEDIA_ROOT, 'csv_uploads', 'Kidney_Raw_BioProbeCountMatrix.csv')
    if Path(probe_expression_file).exists:
        return pandas.read_csv(
            probe_expression_file,
            usecols=[i for i in range(1, 233)],
            index_col='ProbeName',
            delimiter=','
        )

```

<br/>

## <p id="data_analysis">6. Data Analysis</p>

### Statistical Data Analysis:

This goal is best arrived at by using pandas pydata library.

> "**`pandas`** is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language." Pandas Documentation.

With access to data, various analysis procedures can be applied on these data for some given use, e.g... making a dataframe and/or a data series, specifying columns to use, grouping data by a specific index parameter, 

With a DataFrame made, or a Series, much information can be derived or manipulations of a given nature to aid in the processing of results e.g summation, counting, use of arithematic conditions, etc

### Examples of dataframes:

|    | cluster_id   | alias   | data_set                       |
|---:|:------------:|:-------:|:-------------------------------|
| 30 | IN12         | IN12    | barcodeLevelGroup_normalImmune |
| 31 | IN13         | B       | barcodeLevelGroup_normalImmune |
| 32 | IN14         | NK2     | barcodeLevelGroup_normalImmune |
| 33 | IN15         | MST     | barcodeLevelGroup_normalImmune |
| 34 | IN16         | PDC     | barcodeLevelGroup_normalImmune |

<br/>
<br/>

| disease_status   |   ('loq', 'count') |   ('loq', 'mean') |   ('loq', 'std') |   ('loq', 'min') |   ('loq', '25%') |   ('loq', '50%') |   ('loq', '75%') |   ('loq', 'max') |   ('normalization_factor', 'count') |   ('normalization_factor', 'mean') |   ('normalization_factor', 'std') |   ('normalization_factor', 'min') |   ('normalization_factor', '25%') |   ('normalization_factor', '50%') |   ('normalization_factor', '75%') |   ('normalization_factor', 'max') |   ('raw_reads', 'count') |   ('raw_reads', 'mean') |   ('raw_reads', 'std') |   ('raw_reads', 'min') |   ('raw_reads', '25%') |   ('raw_reads', '50%') |   ('raw_reads', '75%') |   ('raw_reads', 'max') |   ('trimmed_reads', 'count') |   ('trimmed_reads', 'mean') |   ('trimmed_reads', 'std') |   ('trimmed_reads', 'min') |   ('trimmed_reads', '25%') |   ('trimmed_reads', '50%') |   ('trimmed_reads', '75%') |   ('trimmed_reads', 'max') |   ('stitched_reads', 'count') |   ('stitched_reads', 'mean') |   ('stitched_reads', 'std') |   ('stitched_reads', 'min') |   ('stitched_reads', '25%') |   ('stitched_reads', '50%') |   ('stitched_reads', '75%') |   ('stitched_reads', 'max') |   ('aligned_reads', 'count') |   ('aligned_reads', 'mean') |   ('aligned_reads', 'std') |   ('aligned_reads', 'min') |   ('aligned_reads', '25%') |   ('aligned_reads', '50%') |   ('aligned_reads', '75%') |   ('aligned_reads', 'max') |   ('duplicated_reads', 'count') |   ('duplicated_reads', 'mean') |   ('duplicated_reads', 'std') |   ('duplicated_reads', 'min') |   ('duplicated_reads', '25%') |   ('duplicated_reads', '50%') |   ('duplicated_reads', '75%') |   ('duplicated_reads', 'max') |   ('sequencing_saturation', 'count') |   ('sequencing_saturation', 'mean') |   ('sequencing_saturation', 'std') |   ('sequencing_saturation', 'min') |   ('sequencing_saturation', '25%') |   ('sequencing_saturation', '50%') |   ('sequencing_saturation', '75%') |   ('sequencing_saturation', 'max') |   ('umiq_30', 'count') |   ('umiq_30', 'mean') |   ('umiq_30', 'std') |   ('umiq_30', 'min') |   ('umiq_30', '25%') |   ('umiq_30', '50%') |   ('umiq_30', '75%') |   ('umiq_30', 'max') |   ('rtsq_30', 'count') |   ('rtsq_30', 'mean') |   ('rtsq_30', 'std') |   ('rtsq_30', 'min') |   ('rtsq_30', '25%') |   ('rtsq_30', '50%') |   ('rtsq_30', '75%') |   ('rtsq_30', 'max') |
|:-----------------|-------------------:|------------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------------:|-----------------:|------------------------------------:|-----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|----------------------------------:|-------------------------:|------------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------:|-----------------------------:|----------------------------:|---------------------------:|---------------------------:|---------------------------:|---------------------------:|---------------------------:|---------------------------:|------------------------------:|-----------------------------:|----------------------------:|----------------------------:|----------------------------:|----------------------------:|----------------------------:|----------------------------:|-----------------------------:|----------------------------:|---------------------------:|---------------------------:|---------------------------:|---------------------------:|---------------------------:|---------------------------:|--------------------------------:|-------------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|------------------------------:|-------------------------------------:|------------------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|-----------------------------------:|-----------------------:|----------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|-----------------------:|----------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|---------------------:|
| DKD              |                131 |           19.7267 |          14.258  |          2.28887 |          10.9341 |          16.3138 |          23.5232 |          71.2849 |                                 131 |                           1.63302  |                           1.74922 |                          0.202788 |                          0.68948  |                           1.01394 |                           1.91522 |                           8.6185  |                      131 |             5.01241e+06 |            4.36641e+06 |                 694121 |            2.4782e+06  |            3.78245e+06 |            5.93801e+06 |            3.17085e+07 |                          131 |                 4.95043e+06 |                4.294e+06   |                     688778 |                2.44848e+06 |                3.75299e+06 |                5.88608e+06 |                3.10706e+07 |                           131 |                  4.89734e+06 |                 4.23438e+06 |                      683752 |                 2.42129e+06 |                 3.72443e+06 |                 5.83802e+06 |                 3.05354e+07 |                          131 |                 4.62566e+06 |                4.05041e+06 |                     653538 |                2.27249e+06 |                3.5099e+06  |                5.48051e+06 |                2.92588e+07 |                             131 |                         355733 |                        302864 |                         19827 |                        150172 |                        281849 |                        432860 |                   1.47169e+06 |                                  131 |                             91.5476 |                            4.6675  |                            73.5934 |                            88.8861 |                            90.7071 |                            97.3293 |                            99.2503 |                    131 |              0.992294 |          0.00326345  |               0.9825 |              0.98855 |              0.9939  |               0.9945 |                0.995 |                    131 |              0.991188 |          0.00388516  |               0.9788 |               0.9869 |               0.9933 |               0.9937 |               0.9943 |
| normal           |                100 |           20.9244 |          12.1599 |          7.20656 |          13.9366 |          16.7528 |          20.8125 |          78.4498 |                                 100 |                           0.978377 |                           0.44989 |                          0.162613 |                          0.662962 |                           1.01394 |                           1.23121 |                           2.46243 |                      100 |             4.41041e+06 |            3.52659e+06 |                 780290 |            2.46474e+06 |            3.21443e+06 |            5.04664e+06 |            1.98133e+07 |                          100 |                 4.37156e+06 |                3.49464e+06 |                     774451 |                2.44429e+06 |                3.18897e+06 |                5.00998e+06 |                1.96258e+07 |                           100 |                  4.3361e+06  |                 3.46787e+06 |                      768703 |                 2.42388e+06 |                 3.16407e+06 |                 4.97351e+06 |                 1.94676e+07 |                          100 |                 4.1106e+06  |                3.23106e+06 |                     730074 |                2.32922e+06 |                3.03052e+06 |                4.74784e+06 |                1.81784e+07 |                             100 |                         411722 |                        312186 |                        109779 |                        230684 |                        289014 |                        429662 |                   1.93504e+06 |                                  100 |                             90.1692 |                            2.84833 |                            80.4187 |                            88.5632 |                            91.3355 |                            91.9104 |                            93.7008 |                    100 |              0.99421  |          0.000598061 |               0.9914 |              0.994   |              0.99435 |               0.9946 |                0.995 |                    100 |              0.99344  |          0.000713364 |               0.9904 |               0.9932 |               0.9936 |               0.9939 |               0.9943 |

</br>
</br>

### Spatial Data Analysis:



<br/>


## <p id="results_visualization">7. Result Visualization</p>

Visualization of data analysis results is the means of communicating the findings from such analyses. **Bokeh**, a python library, offers a variety of nice interactive visual plots which can be rendered by html documents, hence a suitable choice.


Data from a csv or sql table, once read by pandas and a DataFrame made from it, can be collected by bokeh by passing it into a ColumnDataSource which then is a reliable data source for plottings with bokeh. 


---


## <p id="compliance_statement">8. Hackathon Compliance Statement</p>

I have, to the best of my knowledge, adhered to all stated guidelines stated for participation in this Hackathon. The guidelines were clear and I properly discerned every of the mentioned rules, and have kept them.

<br/>


## <p id="installation_procedure">9. Installations & Procedure</p>

Download and Install git

My choice terminal for use during set-up for this project is window's PowerShell (which is a cross platform app, and comes pre-installed in windows devices) and can be downloaded [here](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell?view=powershell-7.1).


Download this project:

### Accessing the code:

The code to this work is uploaded in GitHub in this repository address. It can be downloaded from the specified URL as a zip file or cloned using git. With your command prompt or PowerShell in your directory of choice, you can download the project with the command:

```bash
git clone --depth 1 https://github.com/Wokiri/nanostring.git
```

### Download and Create the needed database

Download the install for your specific platform from the PostgreSQL Binary Download (http://www.postgresql.org/download/)

Once PostgreSQL is installed, launch Application Stack Builder (happens automatically at times). Find a desired version of postgis from the spatial extensions, check it to install.

In the settings.py file found inside nanostring directory, you will see we specified the PostGIS database called "nanostring_DB". We should create it. While still inside this file, modify the password part by replacing the **os.environ.get('DB_PASSWORD')**, with **“your-postgres-password”**

Create the database. In PowerShell, (or simply access the database from postgresql bash) type:

```bash
psql -U postgres
```

When the authorization is successful, go ahead and type:

```bash
CREATE DATABASE “nanostring_DB”;
```

If the creation is successful, we can now prepare and link the project with the database. Type exit to leave the psql shell.


### Create a python virtual environment:

A virtual environment has its own Python binary (which matches the version of the binary that was used to create this environment) and can have its own independent set of installed Python packages in its site directories. This is important due to the fact that the installed packages for each virtual environment don’t interfere with each other, or, it prevents installed packages from affecting system services and other users of the machine. With your command prompt or PowerShell in your directory of choice, a virtual environment can then be created by running:

```bash
C:\Python38\python.exe -m venv nanostringvenv
```

NB:
- This will work only if python is located in the address C:\Python38. If your python 3 isn’t residing in that path, just identify it and replace C:\Python38 with your right address.
- Sometimes, this activation might not be allowed due to safety cautions. But, python is a trusted executable and so we will overide this safety policy by entering the following in the powershell.

```bash
Set-ExecutionPolicy -ExecutionPolicy AllSigned -Scope CurrentUser
```

### Activate the virtual environment

```bash
.\nanostringvenv\Scripts\activate
```

### Download the core needed libraries

```bash
python -m pip install django, pandas, bokeh, sklearn, psycopg2
```

NB:
- If a **SSL: CERTIFICATE_VERIFY_FAILED** error arises, try using this instead:

```bash
python -m pip install --trusted-host=pypi.python.org --trusted-host=pypi.org --trusted-host=files.pythonhosted.org django, pandas, bokeh, sklearn, psycopg2
```

Running this command will install these packages alongside their peer packages. They are all listed in the [requirements text file](./requirements.txt).

**django** Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.

**pandas** pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language.

**bokeh** is a Python library for creating interactive visualizations for modern web browsers. It helps you build beautiful graphics, ranging from simple plots to complex dashboards with streaming datasets. With Bokeh, you can create JavaScript-powered visualizations without writing any JavaScript yourself.

**sklearn**(formerly scikits.learn and also known as sklearn) is a free software machine learning library for the Python programming language.[3] It features various classification, regression and clustering algorithms including support vector machines, random forests, gradient boosting, k-means and DBSCAN, and is designed to interoperate with the Python numerical and scientific libraries NumPy and SciPy.

**Psycopg** is the most popular PostgreSQL database adapter for the Python programming language. Psycopg 2 is both Unicode and Python 3 friendly.

### Install OSGeo4W

GDAL is a translator library for raster and vector geospatial data formats that is released under an X/MIT style Open Source License by the Open Source Geospatial Foundation.

> OSGeo4W or Open Source Geospatial For Windows is a GIS package manager that downloads open source GIS programs and tools and ensures that all of the programs work well together as needed. This is the simplest way to download the libraries needed for GeoDjango.

> Download the installer from https://trac.osgeo.org/osgeo4w/ and run the OSGeo4W Setup program. Select the **Express Web-GIS** Install Click "Next", select a download site for the programs (several servers host the data, try to select one that is geographically closest to you), select all of the options in the proceeding menus and agree to the terms of the licenses. The installation process could take a few minutes as there are several programs to download and install. Click finish once the download/installation process is complete. **https://www.pointsnorthgis.ca/blog/geodjango-gdal-setup-windows-10/**



Then visit https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal

From amongst the wide array of options, you want to chose a gdal version matching the python version used to make and activate your virtual environment, e.g for python 3.8 (as in my case) you download one with cp38 i.e. GDAL‑3.2.2‑cp38‑cp38‑win_amd64.whl; for python 3.7, download one with cp37 i.e. GDAL-3.1.4-cp37-cp37m-win_amd64; and so on and so forth.
Put the downloaded gdal python wheel file in your working folder, then install it with:

```bash
python -m pip install GDAL‑3.2.2‑cp38‑cp38‑win_amd64.whl
```

Next, we will create a new text file called geodjango_setup. Right click on the geodjango.txt file and change the file extension to .bat. Follow these instructions if you are unsure how to change or view the file extensions of your documents.

Open the geodjango_setup.bat file with your favorite text editor, such as Windows built in Notepad or my favorite Notepad++ and copy the code snippet from the Official GeoDjango Documentation or from the example below. You may have to change line 1 from set OSGEO4W_ROOT=C:\OSGeo4W to set OSGEO4W_ROOT=C:\OSGeo4W64, if you have a Windows 64-bit system. You will also have to change the python version in line 2 from set PYTHON_ROOT=C:\Python3X to whatever version of python 3 you have installed, such as set PYTHON_ROOT=C:\Python38 (Find the versions of OSGEO installed and Python installed and adjust the settings accordingly).

e.g `set PYTHON_ROOT=C:\Python38` instead of `set PYTHON_ROOT=C:\Python3X`, or `set OSGEO4W_ROOT=C:\OSGeo4W64` instead of `set OSGEO4W_ROOT=C:\OSGeo4W`

```bash
set OSGEO4W_ROOT=C:\OSGeo4W
set PYTHON_ROOT=C:\Python3X
set GDAL_DATA=%OSGEO4W_ROOT%\share\gdal
set PROJ_LIB=%OSGEO4W_ROOT%\share\proj
set PATH=%PATH%;%PYTHON_ROOT%;%OSGEO4W_ROOT%\bin
reg ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /f /d "%PATH%"
reg ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v GDAL_DATA /t REG_EXPAND_SZ /f /d "%GDAL_DATA%"
reg ADD "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PROJ_LIB /t REG_EXPAND_SZ /f /d "%PROJ_LIB%"
```

If successful, you can at this point confirm that gdal can be accessed by the python environment. In the powershell, type:


```bash
Python manage.py shell 
```

An active python shell will be open, try importing the packages:

```
(venv386) PS D:\Dev> py
Python 3.8.6 (tags/v3.8.6:db45529, Sep 23 2020, 15:52:53) [MSC v.1927 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from osgeo import ogr
>>> from osgeo import gdal
>>>
```

If database creation was successful, we can now prepare to link the project with the database. Type exit() to leave the python shell. 
Then create a migration:

```bash
py manage.py migrate
```

Various tables e.g. auth, amongst others will at this point be created in the database.
Then make a migration, to create all the tables used in the project. 

```bash
py manage.py makemigrations
```


Effect the changes by running another migration:

```bash
py manage.py migrate
```


Your project is now ready. BUT, populate the database with the Digitized spatial data first.

```bash
py manage.py loaddata digitized_data.json
```


Start the server:

```bash
py manage.py runserver
```


In your browser of choice, go to the address:
http://127.0.0.1:8000/
<br/>

---

## <p id="licences">Free & Open Source Softwares Used</p>

**`Bokeh`**:

Bokek is distributed under Berkeley Source Distribution (BSD) license.<br/>
<a href="https://github.com/bokeh/bokeh/blob/branch-2.4/LICENSE.txt">View Bokeh Lisence</a><br/>

<br/>

**`Django`**:

Django licence<br/>
<a href="https://github.com/django/django/blob/main/LICENSE">View Django Lisence</a><br/>

<br/>

<br/>

**`Python`**:

Python History and License.<br/>
<a href="https://docs.python.org/3/license.html">View Python Lisence</a><br/>

<br/>

<br/>

**`Pandas`**:

pandas-dev/pandas is licensed under the BSD 3-Clause "New" or "Revised" License<br/>
<a href="https://github.com/pandas-dev/pandas/blob/master/LICENSE">View Pandas Lisence</a><br/>

<br/>

<br/>

**`openlayers`**:

openlayers/openlayers is licensed under the BSD 2-Clause "Simplified" License<br/>
<a href="https://github.com/pandas-dev/pandas/blob/master/LICENSE">View OL Lisence</a><br/>

<br/>

<br/>

### <p align='right'><a href="#toc">Top</a></p>



---


## Reach Out...

<p align='center'><a href="https://twitter.com/JWokiri"><img height="30" src="https://www.flaticon.com/svg/static/icons/svg/145/145812.svg"></a>

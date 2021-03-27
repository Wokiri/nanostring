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
Using softwares `distributed under a permissive open source license`, I have developed a web app that reads raw data from CSVs files, and for each file, represents the data therein in appropriate visual format (or fomarts) depending on the contents of the file and the expected analysis output, or in a manner I perceived suitable to give somewhat useful information.

### These information might be relayed through:

- Maps: For data with spatial attributes
- Statistical Charts: For data with numerical records (e.g bar charts, pie charts, box plots, tabular records), and
- Relationship Graphs: For data with possible cause-effect entries.

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
9. <a href="#installation">Instalations</a><br/>

  ---
<br/>

## <p id="env_setup">1. Environment Setup</p>

For a successful running of scripts in this project, and indeed a proper functioning of the the overall WebApp, it is highly recommended that all the packages listed in [requirements.txt]() be installed.

At the core of these packages sits python which gives the 'base' platform upon which most of the others depend.

> **"The Python interpreter and the extensive standard library are freely available in source or binary form for all major platforms from the Python Web site, https://www.python.org/, and may be freely distributed."** Python Documentation.



Some of the reliant pachkages include:
Package            | Version
------------------- |---------
bokeh               |2.3.0
dj-rest-auth        |2.1.3
Django              |3.1.4
django-allauth      |0.44.0
django-cors-headers |3.7.0
djangorestframework |3.12.2
GDAL                |3.1.4
pandas              |1.2.3
Pillow              |8.0.1
pip                 |20.3.3
psycopg2            |2.8.6
---------------------------


A detailed process of achieving these installations is covered <a href="#installation">here</a><br/>

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

<br/>

## <p id="data_retrieval">3. Retrieving Data</p>

The [python code (***data_retrieval.py***)](KidneyDataset/data_retrieval.py) which sits in the directory **KidneyDataset** plays the role of accessing the raw txt files from the appropriate [URL](http://nanostring-public-share.s3-website-us-west-2.amazonaws.com/GeoScriptHub/KidneyDataset/) *(given by Nanostring Spatial Omics)*, reading the contents of the text data, cleaning the data and writing both the txt file and a corresponding csv file into the same directory.

In so doing, it perfoms a few checks to minimize the possibilities of errors, i.e:
- Upon execution, the code requires one to input the text name with the extension suffix included (e.g ***Cell_Types_for_Spatial_Decon.txt***). The code will here asses that the name is okay in the sense that there are no spaces between characters and that it has a .txt extension. 
- If this validation is not passed, the appropriate error message(s) is (are) printed out.
- Should the naming be right, the code will attempt to download the data from the remote server and write both the text and csv for it. The assumption here is that the user will input an accurate file name as listed in this [URL](http://nanostring-public-share.s3-website-us-west-2.amazonaws.com/GeoScriptHub/KidneyDataset/).
- If during the running of the code a text file that is sort is found already existing in the present directory, a CSV file will be written from the contents of this txt file and no download would then be necessary.

<br/>


## <p id="data_storage">4. Data storage into the database</p>

### CSV Data:

With django's Object Relational Mapper, the various csv files contents are uploaded into a database either as individual records or as whole files. The smaller files (whose scheema is easy to make)  have been fed and stored in the database as individual records hence making use django's rich Queryset API functionalities.

The larger csv files (with significantly large column records, hence a much more complex schema) are uploaded as a whole into a local storage but whose access is possible by django.

<br/>

### Raster Data:

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

### An example of a dataframe

|    | cluster_id   | alias   | data_set                       |
|---:|:------------:|:-------:|:-------------------------------|
| 30 | IN12         | IN12    | barcodeLevelGroup_normalImmune |
| 31 | IN13         | B       | barcodeLevelGroup_normalImmune |
| 32 | IN14         | NK2     | barcodeLevelGroup_normalImmune |
| 33 | IN15         | MST     | barcodeLevelGroup_normalImmune |
| 34 | IN16         | PDC     | barcodeLevelGroup_normalImmune |

<br/>

### Spatial Data Analysis:



<br/>


## <p id="results_visualization">7. Result Visualization</p>

Visualization of data analysis results is the means of communicating the findings from such analyses. **Bokeh**, a python library, offers a variety of nice interactive visual glyphs which can be rendered by html documents, hence a suitable choice.

### <p align='center'>GIF showing some basic interactive options offered by Bokeh</p>

<p align='center'><img src="" width="1080" alt="Bokeh interactive glyphs"/></p>


---


## <p id="compliance_statement">8. Hackathon Compliance Statement</p>



<br/>


## <p id="licences">9. Installations</p>



<br/>

---

## <p id="licences">Free & Open Source Softwares Used</p>

**`Bokeh`**:

Bokek is distributed under Berkeley Source Distribution (BSD) license.

<br/>

**`Django`**:

Bokek hjkhhgggggggggg

<br/>

**`Django`**:

Bokek hjkhhgggggggggg

<br/>

**`Django`**:

Bokek hjkhhgggggggggg

<br/>

**`Django`**:

Bokek hjkhhgggggggggg

<br/>

**`Django`**:

Bokek hjkhhgggggggggg

<br/>

**`Django`**:

Bokek hjkhhgggggggggg

<br/>

### <p align='right'><a href="#toc">Top</a></p>



---


## Reach Out...

<p align='center'><a href="https://twitter.com/JWokiri"><img height="30" src="https://www.flaticon.com/svg/static/icons/svg/145/145812.svg"></a>
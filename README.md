# <p align='center'>**NANOSTRING SPATIAL OMICS HACKATHON**</p>
## <p>**Hackathon results for [NANOSTRING SPATIAL OMICS](https://nanostring.devpost.com/?ref_content=followed_registered&ref_feature=follow&ref_medium=email&utm_campaign=followed_registered&utm_content=followed_user_registered_for_challenge&utm_medium=email&utm_source=transactional).**</p>

<br/>



<p align='center'><img src="https://dub01pap001files.storage.live.com/y4mfx3F1gQb46H0CDfeaKkBiifqPTH4PLVvjJb9K64mPM75KS5hTzQLXfLfHm8oXYz8iBZCiBAZVhtbZrIWoNtVIWam-F8xjo-l6MSl0dQDzeLNTWMRT0crbTeCM7zlH6f_gP0PjtoLri-rOpoysam8OcxPwV1eNLbD_Pk-Gk-JRXlUQow0eujek41h4PdKLaGN?width=1728&height=1152&cropmode=none" width="1728" alt="Main thumbnail"/></p>

&nbsp;&nbsp;<br/>

### Done & Prepared by: [@JWokiri](https://twitter.com/JWokiri). <br/>

---
<br/>

<h1 id='hackathon_overview'>Hackathon Overview</h1>

---

### **Expectations**:
Creating a graphical representation of data through visual components such as maps, graphs, or other visual formats (e.g. tools that display trends or patterns).
You could create data analysis solutions that collect, interpret, and present data (e.g. tools that identify relationships or detect anomalies). Put your Machine Learning skills to good use and build solutions that use pre-trained models or train a model using the specific dataset.


### **What's Delivered**:
I have developed a web app that reads raw data from CSVs files, and for each file, the app represents it's data in an appropriate visual format (or formarts) depending on the contents of the file and the expected output, or in a manner I perceived suitable to give a somewhat detailed information derived from the data.

## These include:

- Maps: For data with spatial attributes
- Statistical Graphs: For data with numerical records, and
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

1. <a href="#hackathon_overview">Hackathon Overview</a><br/>
2. <a href="#foss">Free & Open Source Softwares Used</a><br/><br/>


**<p>PROJECT IMPLEMENTATION**</p>
   
3. <a href="#env_setup">Environment Setup</a><br/>
4. <a href="#data_retrieval">Retrieving Data</a><br/>
5. <a href="#Enter text name with ext (e.g Cell_Types_for_Spatial_Decon.txt)">Django Project</a><br/>

  ---
<br/>

## <p id="env_setup">1. Environment Setup</p>

For a successful running of scripts in this project, and indeed a proper functioning of the the overall project in general, it is highly recommended that all the packages listed in [lists.txt]() be installed. A detailed process of achieving these installations is covered [here]().

<br/>

## <p id="data_retrieval">2. Retrieving Data</p>

The [python code (***data_retrieval.py***)](KidneyDataset/data_retrieval.py) which sits in the directory **KidneyDataset** plays the role of accessing the raw txt files from the appropriate [URL](http://nanostring-public-share.s3-website-us-west-2.amazonaws.com/GeoScriptHub/KidneyDataset/) given by Nanostring Spatial Omics, reading the contents of the text data, cleaning the data and writing both the txt file and a corresponding csv file into the same directory.

In so doing, it perfoms a few checks to minimize the possibilities of errors, i.e:
- Upon execution, the code requires one to input the text name with the .ext included (e.g ***Cell_Types_for_Spatial_Decon.txt***). The code will here asses that the name is okay in the sense that there are no spaces between characters and that it has a .txt extension.
- If this validation is not passed, the appropriate error message(s) is (are) printed out.
- Should the naming be right, the code will attempt to download the data from the remote server and write both the text and csv for it.
- If during the running of the code a text file that is sort is found in the directory, a CSV file will be writted from the contents of this txt file and no download would then be necessary.

<br/>

## <p id="data_retrieval">4. Django Project</p>
---

## Reach Out...

<p align='center'><a href="https://twitter.com/JWokiri"><img height="30" src="https://www.flaticon.com/svg/static/icons/svg/145/145812.svg">JWokiri</a>
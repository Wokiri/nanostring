'''Downloads data from the URL for each text file.

For every download, this script writes the relevant text file into the local server.
The written textfile is then read and a coresponding csv file is generated in the same location.

The csv file is (later) used by the pydata libraries for data analysis, interpretation and sometimes, visualization.

python packages used are: Path and PurePath from pathlib, urllib.request, pandas
'''

from pathlib import Path, PurePath
import urllib.request
import pandas as pd

fileDir = Path(__file__).parent

def nanostringtextdata_tocsvdata(text_name):

    text_file = PurePath(fileDir, text_name)
    csv_name = text_name.replace('txt', 'csv')
    csv_file = PurePath(fileDir, csv_name)

    df = pd.read_csv(text_file, delimiter=',')
    df.to_csv(csv_file)
    if Path(csv_file).exists:
        print(f"CSV file {csv_file} is successfully created.")
    else:
        print(f"CSV file {csv_file} WAS NOT created.")


def nanostringData(text_name):

    outputname = PurePath(fileDir, text_name)
    name_valid = (text_name.endswith('.txt') and text_name.find(' ') == -1)

    if name_valid and Path(outputname).exists():
        print(f"\nText file {outputname} EXISTS. \nIt has been used to write {text_name.replace('txt', 'csv')}.")
        nanostringtextdata_tocsvdata(text_name)

    elif name_valid:
        dataurl = f'http://nanostring-public-share.s3-website-us-west-2.amazonaws.com/GeoScriptHub/KidneyDataset/{text_name}'

        with open(outputname, mode='w', newline=None) as resultsInTxt:
            with urllib.request.urlopen(dataurl) as nanostringData:
                theData = nanostringData.read()
                # text_data = theData.decode(encoding="utf-8", errors="strict").expandtabs().replace('\r\n', '\n').strip()
                text_data = theData.decode(encoding="utf-8", errors="strict").replace('\t', ',').replace('\r\n', '\n').strip()
                resultsInTxt.write(text_data)

        if Path(outputname).exists:
            print(f"Text file {outputname} is successfully created.")
            nanostringtextdata_tocsvdata(text_name)
        else:
            print(f"Text file {outputname} WAS NOT created.")


    else:
        print(f"Nothing happened! Check that {text_name} is valid and ends with .txt")



txt_name = str(input("Enter text name with ext (e.g Cell_Types_for_Spatial_Decon.txt) \n"))
nanostringData(txt_name)

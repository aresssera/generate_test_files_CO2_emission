# -*- coding: utf-8 -*-
"""getCSV.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/aresssera/generate_test_files_CO2_emission/blob/main/getCSV.ipynb
"""

import pandas as pd # 0.23.0
import numpy as np
import xml.etree.ElementTree as ET
import csv

def get_delimiter(file_path: str) -> str:
    with open(file_path, 'r') as csvfile:
        delimiter = str(csv.Sniffer().sniff(csvfile.read()).delimiter)
        return delimiter

fileName = 'input/combinations.csv'
df = pd.read_csv(fileName, sep = get_delimiter(fileName), on_bad_lines='skip')

tmpNull = 12345
df.iloc[:, 5:10] = df.iloc[:, 5:10].fillna(tmpNull).astype(int).replace(tmpNull, '-')
df = df.replace(np.nan, '-')
print("Are there any NaN values: ", df.isna().any().any())

df.iloc[:, 5:10] = df.iloc[:, 5:10].astype(str)

"""---------------------------------------------------------------------------"""

df['Info manueller Change in DB: vehicleNatureCode '].unique()

"""Map values

"""

dict_VCC = {'N1': '01', 'M1': '30'} # 35 and 38 need to be mapped
dict_CHVC = {'Empty': 'empty', 'OVC-HEV': 'vchev',
             'NOVC-HEV': 'nchev', 'OVC-FCHV': 'cfchv',
             'NOVC-FCHV': 'nfchv'}

def createVIN(row):

  emptyElement = '$'

  newVIN = 'BFE'

  # check for N1
  vcc = row['#VehicleCategoryCode']

  if vcc == 'N1':

    com = row['Info manueller Change in DB: vehicleNatureCode ']

    if com  != '-':
      newVIN = newVIN + com
    else:
      newVIN = newVIN + dict_VCC[vcc]
  else:
    newVIN = newVIN + dict_VCC[vcc]

  newVIN = newVIN + dict_CHVC[row['ClassOfHybridVehicleCode']]

  fuelTypeCode = row['#FuelTypeCode']

  if fuelTypeCode == '-':
    newVIN = newVIN + emptyElement
  else:
    newVIN = newVIN + fuelTypeCode

  for col in ['#FuelCode1','#FuelCode2', '#FuelCode3']:

    val = str(row[col])

    if len(val) < 2:
      if val == '-':
        val = emptyElement + emptyElement
      else:
        val = val + emptyElement

    newVIN = newVIN + val

  return newVIN

df['#VIN'] = df.apply(lambda row: createVIN(row), axis=1)

for i in df['#VIN'].unique():
  if '-' in i:
    print(i)

"""------------------------------------------------------------"""

df['Template'] = df.apply(lambda row: row['Template'].replace("C:\\TESTDATENGENERATOR\\", "templates/"), axis=1)
print(df.head())
df.to_csv('combinations_modified.csv')

valuesToReplace = [col for col in df.columns if col.startswith('#')]
print("valuesToReplace = ", valuesToReplace)

i = 1
for template in df['Template'].unique():

  print(i, ": ", template)

  # all the attribute combinations which need to be with current template
  tmpDF = df[df.Template == template]

  for index, row in tmpDF.iterrows():

    # load template
    tree = ET.parse(template)
    root = tree.getroot()

    for att in valuesToReplace:

      for element in root.iter():
        #if element.text and element.text.startswith(att):
        if element.text == att:
          #if att == '-':
          #  print("empty")
          element.text = row[att]

    # save modified XML file
    tree.write('outputs/' + row['#VIN'] + '.xml', encoding='utf-8', xml_declaration=True)

  i += 1


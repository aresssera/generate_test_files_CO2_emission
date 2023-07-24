import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import csv

fileName = 'input/allPossibleCombinations.csv'
df = pd.read_csv(fileName)
df = df.astype({"#FuelCode1": str}, errors='raise')
df = df.astype({"#FuelCode2": str}, errors='raise')
df = df.astype({"#FuelCode3": str}, errors='raise')

# all attributes which must be replaced
valuesToReplace = [col for col in df.columns if col.startswith('#')]

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

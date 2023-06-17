from typing import List
from Base import Base


import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account


class Slide(Base):
    def __init__(self) -> None:

        # SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/presentations']
        # Load service account credentials
        # SCOPES = ['https://www.googleapis.com/auth/presentations']

        credentials = service_account.Credentials.from_service_account_file("cred.json")

        # Create Google Slides API client
        self.slides_service = build('slides', 'v1', credentials=credentials)


    def convert(self, file: str):
        return 
    
    # def merge(self, files: List[str]):

    def merge(self, presentation_ids: List[str]):

        try:
            slide_list = []
            for id in presentation_ids:
                pres = self.slides_service.presentations().get(presentationId=id).execute()
                slide_list.append({"id": id, "pres": pres})


            # Create a new presentation to merge the slides
            merged_presentation = self.slides_service.presentations().create(body={}).execute()
            merged_presentation_id = merged_presentation['presentationId']

            # Copy slides from the first presentation to the merged presentation
            for slide in slide_list:
                self.slides_service.presentations().pages().copyTo(
                    presentationId=slide["id"],
                    pageObjectId=slide['objectId'],
                    body={'presentationId': merged_presentation_id}
                ).execute()
            print("Merging completed successfully. Merged presentation ID: ", merged_presentation_id)
            return merged_presentation_id

        except Exception as e:
            print("An error occurred while merging presentations:", str(e))


    # Usage example
    # service_account_file = 'path/to/credentials.json'
    # presentation_id1 = 'presentation_id_1'
    # presentation_id2 = 'presentation_id_2'
pres = [
    "1VbTl-LtQhRXqwgEIzQqiTCfy0d34oKqCut7bF7gIX6Q",
    "1Rtw-1OTuAF03cM95tBTgMhhhntPtYdaEnP5YAMlzzSs",
    "1fsXGF2i-p-AAc4pQiSjh_PzqVv5Ar1ABN-d4gX10W2c"
]
# Slide().merge(pres)

from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/presentations',
         'https://www.googleapis.com/auth/spreadsheets']

credentials = service_account.Credentials.from_service_account_file(
    'cred.json')

creds = credentials.with_scopes(SCOPES)

import gslides
from gslides import (
    Frame,
    Presentation,
    Spreadsheet,
    Table,
    Series, Chart
)
import pandas
gslides.initialize_credentials(creds) #BringYourOwnCredentials
prs = Presentation.create(
    name = 'demo pres'
)
spr = Spreadsheet.create(
    title = 'demo spreadsheet',
    sheet_names = ['demo sheet']
)
import pandas as pd

# Define the column names for the DataFrame
column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']

# Define the data for the DataFrame
data = [
    [5.1, 3.5, 1.4, 0.2, 'setosa'],
    [4.9, 3.0, 1.4, 0.2, 'setosa'],
    [4.7, 3.2, 1.3, 0.2, 'setosa'],
    [4.6, 3.1, 1.5, 0.2, 'setosa'],
    [5.0, 3.6, 1.4, 0.2, 'setosa'],
    # ... add more rows for the rest of the Iris dataset
]
from sklearn.datasets import load_iris
# Create the DataFrame
# df = pd.DataFrame(data, columns=column_names)
df = load_iris()
print(prs.presentation_id)
frame = Frame.create(
    df = df,
    spreadsheet_id = spr.spreadsheet_id,   
    sheet_id = spr.sheet_names['demo sheet'],
    sheet_name = 'demo sheet',
    overwrite_data = True
)
sc = Series.scatter()
ch = Chart(
    data = frame.data,       #Passing the data from the frame
    x_axis_column = 'sepal length (cm)',
    series = [sc],           #Passing the series object
    title = 'Demo Chart',
    x_axis_label = 'Sepal Length',
    y_axis_label = 'Petal Width',
    legend_position = 'RIGHT_LEGEND',
)
tbl = Table(
    data = df.head()
)

prs.add_slide(
    objects = [ch, tbl],
    layout = (1,2),             #1 row by 2 columns
    title = "Investigation into Fischer's Iris dataset",
    notes = "Data from 1936"
)


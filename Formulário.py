import pandas as pd
import numpy as np
import streamlit as st
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype
from streamlit_gsheets import GSheetsConnection
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px 
# from oauth2client.service_account import ServiceAccountCredentials
# import gspread

st.set_page_config(
    page_title="Mobilize<>Ifood",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Formulário das Parças do Programa *Meu Diploma*"
    }
)

URL_to_SPREADSHEET = "https://docs.google.com/spreadsheets/d/1sgUe83VbTZPhH5dtBtuGJpk6Pa1tqhUE4QCtOYvZ6ik/edit?gid=280735631#gid=280735631"

# scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# creds = ServiceAccountCredentials.from_json_keyfile_name("mobilize-data.json", scope)
# client = gspread.authorize(creds)
# sheet = client.open('Consolidado V1 - SESI > iFood').worksheet('acompanhamento_geral_atual.')
# data = sheet.get_all_values()
# headers = data[0]
# data = data[1:]


conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(
    spreadsheet= URL_to_SPREADSHEET,
    worksheet="acompanhamento_geral_atual.",
    ttl="10m"
)

print(df)

# colunas = ['Nome','Status','OBS','parceria_ifood','RM','unidade_sesi','CPF', 'email_sesi','phone','email_ifood','Semana 0\n05 a 09/08','1ª semana\n12 a 16/08','2ª semana\n19 a 23/08','3ª semana\n26 a 30/08','4ª semana\n02 a 06/09','5ª semana\n09 a 13/09','6ª semana\n16 a 20/09','já foi a alguma aula?','Foi 1x', 'Foi 2x', 'Foi 3x', 'Foi 4x',
#        'Foi 5x','Foi 6x','Já frenquentou alguma aula presencial? Se sim, qual?']

# df['RM'] = df['RM'].astype(str)
# df['CPF'] = df['CPF'].astype(str)
# df['phone'] = df['phone'].astype(str)
# df['email_sesi'] = df['email_sesi'].astype(str)
# df['email_ifood'] = df['email_ifood'].astype(str)

# st.title("Formulário das Parças")

# with st.form("my_form"):
#     st.write("Inside the form")
#     slider_val = st.slider("Form slider")
#     checkbox_val = st.checkbox("Form checkbox")

#     submitted = st.form_submit_button("Submit")
#     if submitted:
#         st.write("slider", slider_val, "checkbox", checkbox_val)
# st.write("Outside the form")


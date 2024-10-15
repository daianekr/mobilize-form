import pandas as pd
import numpy as np
import streamlit as st
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype
from streamlit_gsheets import GSheetsConnection
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px 
from datetime import datetime
import random
import string
conn2 = st.connection("gsheets2", type=GSheetsConnection)
# Carregar dados da planilha
df1 = conn2.read(
    worksheet="dados-alunos-rds",
    ttl="10m"
)

# Verificar as colunas do DataFrame
st.write(df1.columns)  # Isso mostrará todas as colunas disponíveis
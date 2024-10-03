import pandas as pd
import numpy as np
import streamlit as st
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype
from streamlit_gsheets import GSheetsConnection
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px 

st.set_page_config(
    page_title="Mobilize<>Ifood",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Formulário das Parças do Programa *Meu Diploma*"
    }
)

def formatar_nome(nome):
    partes = nome.split()
    partes_formatadas = [parte.capitalize() for parte in partes]
    return ' '.join(partes_formatadas)

conn1 = st.connection("gsheets1", type=GSheetsConnection)
df1 = conn1.read(
    worksheet="acompanhamento_geral_atual.",
    ttl="10m"
)

conn2 = st.connection("gsheets2", type=GSheetsConnection)
df2 = conn2.read(
    worksheet="teste",
    ttl="10m"
)

colunas = ['Nome','Status','OBS','parceria_ifood','RM','unidade_sesi','CPF', 'email_sesi','phone','email_ifood','Semana 0\n05 a 09/08','1ª semana\n12 a 16/08','2ª semana\n19 a 23/08','3ª semana\n26 a 30/08','4ª semana\n02 a 06/09','5ª semana\n09 a 13/09','6ª semana\n16 a 20/09','já foi a alguma aula?','Foi 1x', 'Foi 2x', 'Foi 3x', 'Foi 4x',
       'Foi 5x','Foi 6x','Já frenquentou alguma aula presencial? Se sim, qual?']

df1['RM'] = df1['RM'].astype(str)
df1['CPF'] = df1['CPF'].astype(str)
df1['phone'] = df1['phone'].astype(str)
df1['email_sesi'] = df1['email_sesi'].astype(str)
df1['email_ifood'] = df1['email_ifood'].astype(str)

st.title("Formulário das Parças")

with st.form("meu_forms"):
    st.write("Formulário de Checagem de informações dos Alunos")
    cpf_input = st.text_input("Digite o CPF:")
    submitted = st.form_submit_button("Confira")
    
    if submitted:
        
        user_info = df1[df1['CPF'] == cpf_input]
        if not user_info.empty:
            st.write("Informações do usuário com CPF:", cpf_input)
            st.markdown("- Nome: " + formatar_nome(user_info['Nome'].values[0]))
            st.markdown("- Status: " + str(user_info['Status'].values[0]))
            st.markdown("- Matricula: " + user_info['RM'].values[0])
            st.markdown("- Unidade: " + user_info['unidade_sesi'].values[0])
            st.markdown("- E-mail: " + user_info['email_sesi'].values[0])
            st.markdown("- Telefone: " + user_info['phone'].values[0])
        else:
            st.write("Nenhum usuário encontrado com o CPF:", cpf_input)
st.write("Fora do Formulário")

with st.form("meu_forms2"):
    st.write("Formulário para escrever as informações dos Alunos")

    text_1 = st.text_input("Teste 1 ")
    text_2 = st.text_input("Teste 2 ")
    text_3 = st.text_input("Teste 3 ")
    
    if st.form_submit_button("Adicionar nova linha"):
        if text_1 and text_2 and text_3:
            # Adicionando nova linha ao DataFrame existente
            new_row = {'Nome': text_1, 'Idade': text_2, 'Profissão': text_3}
            df2 = df2._append(new_row, ignore_index=True)
            
            # Atualizando a planilha com o DataFrame modificado
            conn2.update(
                worksheet="teste",
                data=df2
            )
            st.cache_data.clear()
            st.rerun()
            st.success("Linha adicionada com sucesso!")
        else:
            st.error("Preencha todos os campos para adicionar a nova linha.")


st.write(df2)
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
        'About': "# Formulário das Parças do Programa *Meu Diploma* Turma 1"
    }
)

def formatar_nome(nome):
    partes = nome.split()
    partes_formatadas = [parte.capitalize() for parte in partes]
    return ' '.join(partes_formatadas)

conn2 = st.connection("gsheets2", type=GSheetsConnection)

# Ler os dados da planilha Google
df1 = conn2.read(
    worksheet="dados-alunos",
    ttl="10m"
)

df2 = conn2.read(
    worksheet="teste",
    ttl="10m"
)

# Garantir que as colunas necessárias estão no formato correto
df1['cpf'] = df1['cpf'].astype(str)
df1['phone'] = df1['phone'].astype(str)
df1['email_sesi'] = df1['email_sesi'].astype(str)

st.title("Formulário das Parças")

# Formulário único para buscar CPF e preencher informações
with st.form("formulario_completo", clear_on_submit=True):
    st.write("Formulário de checagem e atendimento dos alunos")
    
    # Parte 1: Buscar informações pelo CPF
    cpf_input = st.text_input("Digite o CPF:")
    
    # Parte 2: Preenchimento do formulário adicional
    text = st.selectbox("Nº da semana do Atendimento", options=["Semana 0", "Semana 1", "Semana 2"])
    text_0 = st.selectbox("O aluno é de qual turma?", options=["Turma 1", "Turma 2"])
    text_1 = st.selectbox("Parça que atendeu:", options=['Fernanda', 'Marina', 'Renata', 'Eliane', 'Karina', 'Elaine'])
    text_2 = st.selectbox("Disparador da conversa:", options=['Resposta ao Chatbot', 'Resposta ao Parça', 'Contato por conta própria'])
    text_3 = st.selectbox("Desenvolveu conversa?", options=['Sim', 'Não'])
    text_4 = st.selectbox("Já frequentou aula presencial?", options=['Sim, em mais de uma semana', 'Não', 'Sim, na semana 0', 'Sim, na semana 1'])
    text_5 = st.selectbox("Reportou dificuldade?", options=['Não se aplica', 'Não tinha todas as informações necessárias', 'Unidade muito longe do local de residência', 'Prejuízo financeiro', 'Dificuldade com o conteúdo do curso', 'Sobrepõe com horário de alta demanda no trabalho', 'Não tenho dinheiro para me locomover ou me alimentar', 'Problema de saúde'])
    text_6 = st.selectbox("Comentários:", options=["Não se aplica", "Questões sobre dia, horário ou endereço", "Falta de informação", "Problemas de cadastro", "Vai numa próxima aula", "Problemas pessoais", "Está tudo bem!", "Dúvidas sobre os R$ 60", "Elogios ao programa", "Dúvidas e comentários sobre aulas", "Benefícios iFood e Sesi"])
    text_7 = st.text_input("Detalhes do Aluno:")
    text_8 = st.text_input("Observações do atendimento:")
    text_9 = st.selectbox("Precisa encaminhar esse caso?", options = ["Não", "Sim", "Não se Aplica"])

    # Botão para submeter
    if st.form_submit_button("Submeter Resposta"):
        # Exibir o spinner enquanto os dados estão sendo gravados
        with st.spinner('Gravando dados, por favor aguarde...'):
            # Verifica se o CPF foi inserido e buscado no DataFrame
            user_info = df1[df1['cpf'] == cpf_input]
            
            if not user_info.empty:
                # Combina os dados do formulário com os dados buscados (df1)
                new_row = {
                    'Nome': formatar_nome(user_info['Nome'].values[0]),
                    'Status': user_info['Status'].values[0],
                    'Parceria_ifood': user_info['parceria_ifood'].values[0],
                    'Unidade_sesi': user_info['unidade_sesi'].values[0],
                    'CPF': user_info['cpf'].values[0],
                    'E-mail': user_info['email_sesi'].values[0],
                    'Telefone': user_info['phone'].values[0],
                    'Atendimento': text,
                    'Turma': text_0,
                    'Parça que atendeu': text_1,
                    'Disparador da conversa': text_2,
                    'Desenvolveu conversa?': text_3,
                    'Já frequentou aula presencial?': text_4,
                    'Reportou dificuldade?': text_5,
                    'Comentários': text_6,
                    'Detalhes do Aluno': text_7,
                    'Observações do atendimento': text_8,
                    'Precisa encaminhar esse caso?': text_9
                }

                # Adicionar a nova linha ao DataFrame
                df2 = df2._append(new_row, ignore_index=True)

                # Atualizar a planilha com o novo DataFrame
                conn2.update(
                    worksheet="teste",
                    data=df2
                )

                # Limpar o cache de dados e recarregar
                st.cache_data.clear()
                st.rerun()
                st.success("Informações atualizadas com sucesso!")
            else:
                st.error("Nenhum usuário encontrado com o CPF informado.")


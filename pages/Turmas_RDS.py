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


# Usuários com senhas aleatórias
USER_CREDENTIALS = {
    "Fernanda": 'teste1',
    "Marina": 'teste2',
    "Renata": 'teste3',
    "Eliane": 'teste4',
    "Karina": 'teste5',
    "Elaine": 'teste6',
}


# Configurações da página
st.set_page_config(
    page_title="Mobilize<>Ifood",
    page_icon="📑",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Formulário das Parças do Programa *Meu Diploma*"
    }
)

# Função para formatar o nome corretamente
def formatar_nome(nome):
    partes = nome.split()
    partes_formatadas = [parte.capitalize() for parte in partes]
    return ' '.join(partes_formatadas)

# Conexão com Google Sheets
conn2 = st.connection("gsheets2", type=GSheetsConnection)

# Carregar dados das planilhas
df1 = conn2.read(
    worksheet="dados-alunos-rds",
    ttl="10m"
)

df2 = conn2.read(
    worksheet="teste",
    ttl="10m"
)

# Formatar colunas como strings
df1['CPF'] = df1['CPF'].astype(str)
df1['Celular'] = df1['Celular'].astype(str)
df1['E-mail'] = df1['E-mail'].astype(str)

# Função de autenticação
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    # Formulário de login
    st.title("Login")

    username = st.text_input("Nome")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.authenticated = True
            st.session_state.username = username  # Armazenar o username na sessão
            st.success(f"Você está logada(o) como {username}")
            return True
        else:
            st.error("Nome ou Senha incorretos")

    return False

# Conteúdo principal do app
if check_password():
    # Mostrar conteúdo protegido após login
    st.title("Formulário das Parças")

    if 'user_info' not in st.session_state:
        st.session_state.user_info = None

    # Formulário de consulta de alunos
    with st.form("meu_forms"):
        st.write("Formulário de checagem de informações dos alunos")
        cpf_input = st.text_input("Digite o CPF:")
        submitted = st.form_submit_button("Confirma")
        
        if submitted:
            user_info = df1[df1['CPF'] == cpf_input]
            if not user_info.empty:
                st.write("Informações do aluno com CPF:", cpf_input)
                st.markdown("- Nome: " + formatar_nome(user_info['Nome completo'].values[0]))
                st.markdown("- Ciclo de estudos: " + str(user_info['Ciclo de estudos'].values[0]))
                st.markdown("- Unidade: " + user_info['Unidade'].values[0])
                st.markdown("- E-mail: " + user_info['E-mail'].values[0])
                st.markdown("- Telefone: " + user_info['Celular'].values[0])
                st.session_state.user_info = user_info
            else:
                st.write("Nenhum aluno encontrado com o CPF:", cpf_input)
                st.session_state.user_info = None

    # Formulário de atendimento
    with st.form("meu_forms2", clear_on_submit=True):
        st.write("Formulário para escrever as informações de atendimento dos alunos")

        text_2 = st.selectbox("Motivo da Mensagem:", options=['Resposta a uma campanha', 'Resposta a uma parça', 'Contato por conta própria', 'Registro de disparo'])
        text_3 = st.selectbox("Campanha atrelada:", options=['Campanha 1', 'Campanha 2', 'Campanha 3', 'Campanha 3'])
        # Pergunta se frequentou aula presencial (Sim ou Não)
        frequentou_aula = st.selectbox("Frequentou aula presencial?", options=['Sim', 'Não'])

        # Se a resposta for "Sim", aparece a pergunta condicional
        if frequentou_aula == 'Sim':
            quantas_vezes = st.selectbox("Quantas vezes?", options=['1x', '2x', '3x ou mais'])

        text_6 = st.selectbox("Comentários:", options=["Dúvidas sobre o curso", " Dúvidas sobre a gameficação", "Dúvidas e comentários sobre as aulas", "Problemas de cadastro", "Dificuldades financeiras", "Problemas pessoais ou de saúde"])
        text_7 = st.text_input("Detalhes do atendimento:")
        text_8 = st.text_input("Observações sobre o aluno:")


        text_9 = st.text_input("Precisa encaminhar esse caso?", help="Este campo é obrigatório para submissão.")
        
        if not text_9: 
            st.error("Por favor, preencha o campo 'Precisa encaminhar esse caso?'.")

        if st.form_submit_button("Submeter Resposta"):
            if not text_9: 
                st.error("Por favor, preencha o campo 'Precisa encaminhar esse caso?' para submeter o formulário.")
            else:
                with st.spinner('Gravando dados, por favor aguarde...'):
                    if st.session_state.user_info is not None:
                        user_info = st.session_state.user_info

                        # Adicionando nova linha com a data e hora do preenchimento
                        new_row = {
                            'Nome': formatar_nome(user_info['Nome'].values[0]),
                            'Ciclo de estudos': user_info['Ciclo de estudos'].values[0],
                            'Unidade': user_info['Unidade'].values[0],
                            'CPF': user_info['CPF'].values[0],
                            'E-mail': user_info['E-mail'].values[0],
                            'Telefone': user_info['Celular'].values[0],
                            'Motivo da Mensagem:': text_2,
                            'Campanha atrelada:': text_3,
                            'Frequentou aula presencial?': frequentou_aula,
                            'Quantas vezes?': quantas_vezes if frequentou_aula == 'Sim' else '',
                            'Comentários': text_6,
                            'Detalhes do Aluno': text_7,
                            'Observações do atendimento': text_8,
                            'Precisa encaminhar esse caso?': text_9,  # Campo obrigatório
                            'Quem atendeu?': st.session_state.username,  # Usar o username logado
                            'extract_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Data e hora de preenchimento
                        }

                        df2 = df2._append(new_row, ignore_index=True)

                        # Atualizar planilha
                        conn2.update(
                            worksheet="teste",
                            data=df2
                        )

                        st.cache_data.clear()
                        st.rerun()
                        st.success("Informações atualizadas com sucesso!")
                    else:
                        st.error("Nenhuma informação de CPF encontrada. Verifique antes de submeter.")
else:
    st.write("Por favor, faça login para acessar o app.")


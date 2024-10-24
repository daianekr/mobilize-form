import pandas as pd
import numpy as np
import streamlit as st
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype
from streamlit_gsheets import GSheetsConnection
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px 
from datetime import datetime, timedelta
import random
import string

USER_CREDENTIALS = st.secrets["USER_CREDENTIALS"]

st.set_page_config(
    page_title="Mobilize<>Ifood",
    page_icon="📑",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Formulário das Parças do Programa *Meu Diploma*"
    }
)


def formatar_nome(nome):
    partes = nome.split()
    partes_formatadas = [parte.capitalize() for parte in partes]
    return ' '.join(partes_formatadas)


conn2 = st.connection("gsheets2", type=GSheetsConnection)


df1 = conn2.read(
    worksheet="dados-alunos",
    ttl="10m"
)

df2 = conn2.read(
    worksheet="alunos-sem-cadastro",
    ttl="10m"
)

df3 = conn2.read(
    worksheet="dados-alunos",
    ttl="10m"
)

df3['CPF'] = df3['CPF'].apply(lambda x: str(int(x)) if isinstance(x, float) else str(x)).str.strip()
df3['phone'] = df3['phone'].astype(str).fillna("").str.strip()
df3['E-mail'] = df3['E-mail'].astype(str).fillna("").str.strip()

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.title("Login")

    username = st.text_input("Nome")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.authenticated = True
            st.session_state.username = username  
            st.success(f"Você está logada(o) como {username}")
            return True
        else:
            st.error("Nome ou Senha incorretos")

    return False

if check_password():
    st.title("Formulário das Parças")

    if 'user_info' not in st.session_state:
        st.session_state.user_info = None

    with st.form("meu_forms"):
        st.write("Formulário de checagem de informações dos alunos")
        cpf_input = st.text_input("Digite o CPF:", key="cpf_input_form1")
        submitted = st.form_submit_button("Confirma")

        if submitted:
            user_info = df3[df3['CPF'] == cpf_input]
            if not user_info.empty:
                st.write("Informações do aluno com CPF:", cpf_input)
                nome_input = formatar_nome(user_info['Nome'].values[0])
                ciclo_input = str(user_info['Ciclo'].values[0])
                unidade_input = user_info['Unidade'].values[0]
                email_input = user_info['E-mail'].values[0]
                telefone_input = user_info['phone'].values[0]
                st.session_state.user_info = user_info
            else:
                st.warning("Nenhum aluno encontrado com o CPF. Preencha os campos manualmente.")
                nome_input = ""
                ciclo_input = ""
                unidade_input = ""
                email_input = ""
                telefone_input = ""

            # Armazenar os valores nos estados da sessão
            st.session_state.cpf_input = cpf_input  # Agora garantimos que o CPF digitado seja armazenado
            st.session_state.nome_input = nome_input
            st.session_state.ciclo_input = ciclo_input
            st.session_state.unidade_input = unidade_input
            st.session_state.email_input = email_input
            st.session_state.telefone_input = telefone_input

    # Verificar se o CPF foi armazenado corretamente no estado da sessão
    cpf_input = st.session_state.get('cpf_input', "")

    # Formulário para permitir edição manual, se necessário
    nome_input = st.text_input("Nome", value=st.session_state.get('nome_input', ''), key="nome_input_manual")
    ciclo_input = st.text_input("Ciclo", value=st.session_state.get('ciclo_input', ''), key="ciclo_input_manual")
    unidade_input = st.text_input("Unidade", value=st.session_state.get('unidade_input', ''), key="unidade_input_manual")
    email_input = st.text_input("E-mail", value=st.session_state.get('email_input', ''), key="email_input_manual")
    telefone_input = st.text_input("Telefone", value=st.session_state.get('telefone_input', ''), key="telefone_input_manual")

    with st.form("meu_forms2", clear_on_submit=True):
        st.write("Formulário para escrever as informações de atendimento dos alunos")

        text_2 = st.selectbox("Motivo da Mensagem:", options=['Resposta a uma campanha', 'Resposta a uma parça', 'Contato por conta própria', 'Registro de disparo'], key="motivo_mensagem")
        text_3 = st.selectbox("Campanha atrelada:", options=[' ', 'Campanha 1', 'Campanha 2', 'Campanha 3'], key="campanha_atrelada")
        frequentou_aula = st.selectbox("Frequentou aula presencial?", options=['Sim', 'Não'], key="frequentou_aula")

        if frequentou_aula == 'Sim':
            quantas_vezes = st.selectbox("Quantas vezes?", options=[' ', '1x', '2x', '3x ou mais'], key="quantas_vezes")
        else:
            quantas_vezes = ''

        text_6 = st.selectbox("Comentários:", options=["Dúvidas sobre o curso", " Dúvidas sobre a gameficação", "Dúvidas e comentários sobre as aulas", "Problemas de cadastro", "Dificuldades financeiras", "Problemas pessoais ou de saúde"], key="comentarios")
        text_7 = st.text_input("Detalhes do atendimento:", key="detalhes_atendimento")
        text_8 = st.text_input("Observações sobre o aluno:", key="observacoes_aluno")

        text_9 = st.text_input("Precisa encaminhar esse caso?", help="Este campo é obrigatório para submissão.", key="precisa_encaminhar")

        if not text_9:
            st.error("Por favor, preencha o campo 'Precisa encaminhar esse caso?'.")

        if st.form_submit_button("Submeter Resposta"):
            if not text_9:
                st.error("Por favor, preencha o campo 'Precisa encaminhar esse caso?' para submeter o formulário.")
            else:
                with st.spinner('Gravando dados, por favor aguarde...'):
                    # Verifica se há dados preenchidos no primeiro formulário (CPF encontrado ou preenchido manualmente)
                    if cpf_input:  # Certifique-se de que o CPF está no estado da sessão
                        new_row = {
                            'Nome': nome_input if nome_input else "",
                            'Ciclo': ciclo_input if ciclo_input else "",
                            'Unidade': unidade_input if unidade_input else "",
                            'CPF': cpf_input,  # Sempre usar o CPF digitado
                            'E-mail': email_input if email_input else "",
                            'Telefone': telefone_input if telefone_input else "",
                            'Motivo da Mensagem:': text_2,
                            'Campanha atrelada:': text_3,
                            'Frequentou aula presencial?': frequentou_aula,
                            'Quantas vezes?': quantas_vezes,
                            'Comentários': text_6,
                            'Detalhes do Aluno': text_8,
                            'Observações do atendimento': text_7,
                            'Precisa encaminhar esse caso?': text_9,
                            'Quem atendeu?': st.session_state.username,
                            'extract_at': (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
                        }

                        # Atualizar os dados na planilha
                        df2 = df2._append(new_row, ignore_index=True)

                        conn2.update(
                            worksheet="alunos-sem-cadastro",
                            data=df2
                        )

                        st.cache_data.clear()
                        st.rerun()
                        st.success("Informações atualizadas com sucesso!")
                    else:
                        st.error("CPF não foi encontrado ou preenchido. Verifique antes de submeter.")
else:
    st.write("Por favor, faça login para acessar o app.")
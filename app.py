import streamlit as st
import random
import pandas as pd
import uuid
import sqlite3

introducao = """Olá, meu nome é Juliana, e meu TCC tem como objetivo avaliar se o modelo de LLM llama 3 é capaz de auxiliar no aprendizado de alunos iniciantes em lógica de programação.
                
Pedimos para o modelo comentar soluções de exercícios de alunos de Computação 1 na UFRJ e gostaríamos de avaliar 
se os comentários que ele deu foram adequados e úteis para um aluno iniciante. 
                
Abaixo serão mostradas 3 soluções de alunos, e os respectivos problemas aos quais as soluções se referem, 
e dois comentários diferentes que o modelo deu para cada. A ideia é avaliar cada comentário em uma escala de 1 a 5, 
e escolher qual comentário é mais apropriado para a solução."""

questao_carro = """Um grupo de amigos deseja fazer uma viagem e decidiram ir de carro.

Pelas regras rodoviárias, um veículo convencional tem a capacidade de transportar até 5 passageiros, porém há veículos com outras capacidades.


Construa uma função em Python chamada **carros** para calcular e retornar o número exato de carros necessários para esta viagem, considerando que seja dado como entrada o número de pessoas. 
Caso os veículos considerados sejam de capacidades não convencionais, será dado também como entrada a capacidade dos veículos."""

questao_aviao = """Para descontrair os alunos após as provas da OBI, a Diretora da escola organizou um campeonato de aviões\
                 de papel. 
                 Cada aluno participante receberá uma certa quantidade de folhas de um papel especial para fazer \
                os seus modelos de aviões. A quantidade de folhas que cada aluno deverá receber ainda não foi determinada.
                Considere, por exemplo, que a Diretora comprou 100 folhas \
                de papel especial, e que há 33 competidores. Se os juízes decidirem que cada competidor tem direito a \
                três folhas de papel, a quantidade comprada pela diretora é suficiente. Mas se os juízes decidirem que \
                cada competidor tem direito a quatro folhas, a quantidade comprada pela diretora não seria suficiente. 
                Você deve escrever uma função definida por avioes(competidores, papel_comprado, papel_competidor) que, \
                dados o número de competidores, o número de folhas de papel especial compradas pela Diretora e o número \
                de folhas que cada competidor deve receber, determine se o número de folhas comprado pela Diretora é \
                suficiente.
                Entrada: Três números inteiros representando respectivamente o \
                        número de competidores, a quantidade de folhas de papel especial compradas pela Diretora e a\
                         quantidade de folhas de papel especial que cada competidor deve receber. 
                Saída: A sua função deve retornar 'Suficiente' se a quantidade de folhas compradas pela Diretora for \
                        suficiente, ou 'Insuficiente' caso contrário. 
                Exemplos: 
                Entrada: 10,100,10 
                Saída: 'Suficiente' 
                Entrada: 10,90,10 
                Saída: 'Insuficiente' 
                Entrada: 5,40,2 
                Saída: 'Suficiente'"""

conexao = sqlite3.connect("dados_origem.db")
df_comentarios = pd.read_sql_query("SELECT * FROM comentarios_modelo", conexao)
conexao.close()

df_avioes = pd.read_csv("735avioes_solucoes.csv")
df_carros = pd.read_csv("839carros_solucoes.csv")

solucoes = {2: df_avioes["solution"].to_list(), 1: df_carros["solution"].to_list()}

questoes = {1: questao_carro, 2: questao_aviao}

total_paginas = 5

if "num_problema_1" not in st.session_state:
    opcoes_problema = [1, 2]
    num_problema_1 = random.choice(opcoes_problema)
    st.session_state.num_problema_1 = num_problema_1

if "num_solucao_1" not in st.session_state:
    opcoes_solucao = [1, 2, 3, 4]
    num_solucao_1 = random.choice(opcoes_solucao)
    st.session_state.num_solucao_1 = num_solucao_1

if "configuracao_1" not in st.session_state:
    opcoes_prompt = [1, 2, 3]
    configuracao_1_1 = random.choice(opcoes_prompt)
    st.session_state.configuracao_1_1 = configuracao_1_1

if "configuracao_2" not in st.session_state:
    configuracao_1_2 = random.choice([i for i in opcoes_prompt if i != configuracao_1_1])
    st.session_state.configuracao_1_2 = configuracao_1_2

def pagina_atual():
    if 'pagina' not in st.session_state:
        st.session_state.pagina = 1

    if 'navegar' not in st.session_state:
        st.session_state.navegar = None  # Controla a navegação

# Funções para navegar entre páginas
def proxima_pagina():
    st.session_state.pagina += 1

def pagina_anterior():
    st.session_state.pagina -= 1

pagina_atual()

# Variável para mensagem de erro
erro = st.empty()

# Lógica de navegação
if st.session_state.navegar == 'proxima':
    proxima_pagina()
    st.session_state.navegar = None  # Reseta o estado de navegação
    
elif st.session_state.navegar == 'anterior':
    pagina_anterior()
    st.session_state.navegar = None  # Reseta o estado de navegação

# Página 1: Dados Pessoais
if st.session_state.pagina == 1:
    
    st.title("Formulário para a pesquisa sobre LLM's e educação")    
    #st.markdown(introducao)
    st.markdown(
    f"""
    <div style="border: 1px solid #d0d0d0; padding: 10px; border-radius: 5px;">
        {introducao}
    </div>
    """,
    unsafe_allow_html=True,
)

    with st.form(key='form_pagina1'):

        materias_lecionadas = st.multiselect(
            "Quais as principais matérias você leciona/lecionou? (*)",
            options=["Introdução à Programação", "Banco de Dados", "Algoritmos e Estruturas de Dados", 
                    "Redes de Computadores", "Inteligência Artificial", "Cibersegurança", "Computação Gráfica",
                    "Engenharia de Software", "Sistemas Operacionais", "Programação Orientada a Objetos", "Outras"],
            key="materias_lecionadas"
        )

        materias_lecionadas_extra = st.text_input("Caso tenha escolhido a opção 'Outras', escreva abaixo quais outras matérias que você leciona/lecionou:", key = "materias_lecionadas_extra")

        tempo_lecionando = st.radio(
            "Quantos anos você tem de experiência lecionando disciplinas relacionadas à computação? (*)",
            options=["0-5 anos", "6-10 anos", "11-15 anos", "16-20 anos", "Mais de 20 anos"],
            key="tempo_lecionando")

        onde_leciona = st.multiselect(
            "Em qual ou em quais níveis de ensino você leciona ou lecionou? (*)",
            options=["Ensino Básico e Tecnológico", "Ensino Superior", "Pós-Graduação Lato Sensu (MBA)", "Pós-graduação Stricto Sensu"],
            key="onde_leciona"
        )

        proxima = st.form_submit_button("Próxima")

    if proxima:
        st.session_state.navegar = 'proxima'

        #     if not tempo_leciona or not onde_leciona or not(materias_lecionadas or materias_lecionadas_extra):
        #         erro.error("Por favor, preencha todos os campos obrigatórios!")
        #     else:
        #         erro.empty()
        #         st.session_state.navegar = 'proxima'

elif st.session_state.pagina == 2:

    str_problema_1 = questoes[st.session_state.num_problema_1]
    str_solucao_1 = solucoes[st.session_state.num_problema_1][st.session_state.num_solucao_1-1]

    condicoes_1 = (df_comentarios["problema"] == st.session_state.num_problema_1) & (df_comentarios["solucao"] == st.session_state.num_solucao_1) & (df_comentarios["prompt"] == st.session_state.configuracao_1_1)
    comentario_1 = df_comentarios.loc[condicoes_1, "comentario_llm"].iloc[0]
    comentario_1_id = df_comentarios.loc[condicoes_1, "id"].iloc[0]

    condicoes_2 = (df_comentarios["problema"] == st.session_state.num_problema_1) & (df_comentarios["solucao"] == st.session_state.num_solucao_1) & (df_comentarios["prompt"] == st.session_state.configuracao_1_2)
    comentario_2 = df_comentarios.loc[condicoes_2, "comentario_llm"].iloc[0]
    comentario_2_id = df_comentarios.loc[condicoes_2, "id"].iloc[0]


    with st.form(key='form_pagina2'):
        
        st.header("Questão e Solução 1")
        st.markdown("Avalie dois comentários diferentes feitos pelo modelo considerando a corretude do comentários e se ele é adequado para o perfil de um aluno que está iniciando seus estudos em programação.")

        st.markdown("### Enunciado")
        #st.write(str_problema_1)
        st.markdown(
            f"""
            <div style="border: 1px solid #4a4a4a; padding: 10px; border-radius: 5px;">
                {str_problema_1}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### Solução do aluno")
        st.code(str_solucao_1, language='python')

        st.markdown("### Comentário 1 do modelo")
        #st.markdown(comentario_1)
        st.markdown(
            f"""
            <div style="border: 1px solid #4a4a4a; padding: 10px; border-radius: 5px;">
                {comentario_1}
            </div>
            """,
            unsafe_allow_html=True,
        )

        nota_1 = st.radio(
            "Considerando a corretude do comentário e se ele se adequa a uma aluno iniciante em programação, o quanto você concorda com esse comentário? (*)",
            options=["Concordo Totalmente", "Concordo Parcialmente", "Indiferente ou Neutro","Discordo Parcialmente", "Discordo Totalmente"],
            key="nota_1_1"
        )

        st.markdown("### Comentário 2 do modelo")
        #st.markdown(comentario_2)
        st.markdown(
            f"""
            <div style="border: 1px solid #4a4a4a; padding: 10px; border-radius: 5px;">
                {comentario_2}
            </div>
            """,
            unsafe_allow_html=True,
        )        

        nota_2 = st.radio(
            "Considerando a corretude do comentário e se ele se adequa a uma aluno iniciante em programação, o quanto você concorda com esse comentário? (*)",
            options=["Concordo Totalmente", "Concordo Parcialmente", "Indiferente ou Neutro","Discordo Parcialmente", "Discordo Totalmente"],
            key="nota_1_2"
        )

        preferencia_1 = st.radio(
            "Entre os dois comentários, qual você prefere?(*)",
            options=["Comentário 1", "Comentário 2"], key="preferencia_1"
        )

        texto_1 = st.text_area(
                    label="Se puder, escreva o que te fez escolher um comentário a outro:", 
                    height=150,  # Define a altura da caixa
                    placeholder="Escreva algo...",
                    key= "texto_1"
                )

        col1, col2, col3 = st.columns([1, 1, 1])

        st.session_state.materias_lecionadas = st.session_state.materias_lecionadas
        st.session_state.materias_lecionadas_extra = st.session_state.materias_lecionadas_extra
        st.session_state.tempo_lecionando = st.session_state.tempo_lecionando
        st.session_state.onde_leciona = st.session_state.onde_leciona
        st.session_state.comentario_1_id = comentario_1_id
        st.session_state.comentario_2_id = comentario_2_id

        with col1:
            voltar = st.form_submit_button("Voltar")

        with col2:
            proxima = st.form_submit_button("Próxima")

        with col3:
            enviar = st.form_submit_button("Enviar")

    if voltar:
        st.session_state.navegar = 'anterior'

    if proxima or enviar:
            id_usuario = str(uuid.uuid4())

            # if not interesse == "Outra":
            #         erro.error("Por favor, especifique seu interesse!")
            # else:
                #erro.empty()
    if proxima:
            st.session_state.navegar = 'proxima'
        
    if enviar:

            # tupla_ids = (comentario_1_id, comentario_2_id, comentario_3_id, comentario_4_id, comentario_5_id, comentario_6_id)
            # conexao = sqlite3.connect('dados_origem.db')
            # cursor = conexao.cursor()
            # cursor.execute(
            #     "UPDATE comentarios_modelo SET vezes_sorteado = vezes_sorteado + 1 WHERE id_disciplina IN (?, ?, ?, ?, ?, ?)",
            #     (tupla_ids,)
            # )

            # # Confirmando e fechando a conexão
            # conexao.commit()
            # conexao.close()
            
            # tupla_ids = (st.session_state.comentario_1_id, st.session_state.comentario_2_id)
            # print(tupla_ids)
            # conexao = sqlite3.connect('dados_origem.db')
            # cursor = conexao.cursor()
            # cursor.execute(
            #     "UPDATE comentarios_modelo SET vezes_sorteado = vezes_sorteado + 1 WHERE id IN (?, ?)",
            #     tupla_ids
            # )
            # conexao.commit()
            # conexao.close()

            dados_resultados = {"id_usuario": id_usuario, "num_anos_leciona": st.session_state.tempo_lecionando, 
                                "nm_materias_extra": st.session_state.materias_lecionadas_extra,
                                "questao_1": st.session_state.num_problema_1, "sol_1": st.session_state.num_solucao_1,
                                "config_1_1": st.session_state.configuracao_1_1, 
                                "nota_1_1": st.session_state.nota_1_1,"config_1_2": st.session_state.configuracao_1_2, 
                                "nota_1_2":st.session_state.nota_1_2, "preferencia_1": st.session_state.preferencia_1,
                                "texto_1": st.session_state.texto_1}
            
            print(dados_resultados)
            
            conexao = sqlite3.connect('resultados_teste.db')

            cursor = conexao.cursor()

            colunas = ', '.join(dados_resultados.keys())  
            placeholders = ', '.join(['?'] * len(dados_resultados))  # Gera '?, ?, ?, ?'
            valores = tuple(dados_resultados.values()) 

            # 5. Inserir o dicionário como uma nova linha na tabela
            sql = f"INSERT INTO resultados ({colunas}) VALUES ({placeholders})"
            cursor.execute(sql, valores)


            usuario_disciplinas = [{"id_usuario":id_usuario, "nm_disciplina": v} for v in st.session_state.materias_lecionadas]
            
            for dict_disciplinas in usuario_disciplinas:
                colunas = ', '.join(dict_disciplinas.keys())  
                placeholders = ', '.join(['?'] * len(dict_disciplinas))  # Gera '?, ?, ?, ?'
                valores = tuple(dict_disciplinas.values()) 

                # 5. Inserir o dicionário como uma nova linha na tabela
                sql = f"INSERT INTO usuario_disciplinas ({colunas}) VALUES ({placeholders})"
                cursor.execute(sql, valores)
            
            usuario_onde_leciona = [{"id_usuario":id_usuario, "nm_onde_leciona": v} for v in st.session_state.onde_leciona]

            for dict_onde_leciona in usuario_onde_leciona:
                colunas = ', '.join(dict_onde_leciona.keys())  
                placeholders = ', '.join(['?'] * len(dict_onde_leciona))  # Gera '?, ?, ?, ?'
                valores = tuple(dict_onde_leciona.values()) 

                # 5. Inserir o dicionário como uma nova linha na tabela
                sql = f"INSERT INTO usuario_onde_leciona ({colunas}) VALUES ({placeholders})"
                cursor.execute(sql, valores)

            # Confirmando e fechando a conexão
            conexao.commit()
            conexao.close()
            # resultados = [
            #     (,), ("Banco de Dados",), ("Algoritmos e Estruturas de Dados",), 
            #     ("Redes de Computadores",), ("Inteligência Artificial",), ("Cibersegurança",), ("Computação Gráfica",),
            #     ("Engenharia de Software",), ("Sistemas Operacionais",), ("Programação Orientada a Objetos",)
            #     ]

            # cursor.executemany("INSERT INTO disciplinas (nm_disciplina) VALUES (?)", disciplinas)


st.markdown(
    f"""
    <div style='text-align: right; margin-top: 5px;'>
        Página {st.session_state.pagina} de {total_paginas}
    </div>
    """,
    unsafe_allow_html=True
)





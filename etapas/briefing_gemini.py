import streamlit as st
import google.generativeai as genai
import uuid
import os
from pymongo import MongoClient
from datetime import datetime
import os
from tavily import TavilyClient
from pymongo import MongoClient
import requests

oq_brief = '''É O DOCUMENTO QUE
CONSOLIDA TODA INFORMAÇÃO
RELEVANTE E NECESSÁRIA
PARA A EXECUÇÃO DO
TRABALHO.

serve como guia, inspiração e também como destrave para
o processo estratégico e criativo.


ANTES DE INICIAR QUALQUER TRABALHO DE
COMUNICAÇÃO/ESTRATÉGIA É IMPORTANTE
QUE O PLANEJADOR TENHA O BRIEFING
CORRETO PARA CONSEGUIR CONSTRUIR A
MELHOR SOLUÇÃO PARA O OBJETIVO.


UM BOM BRIEFING DEVE SER

CLARO
CONCISO
LINEAR
INSPIRADOR

As informações precisam estar detalhadas
de forma precisa, com uma narrativa que
seja de fácil entendimento e que fique
evidente qual é o problema a ser
resolvido.

DESAFIOS PARA A
CONSTRUÇÃO DE UM BRIEFING
POTENTE:

INFORMAÇÕES QUE SÃO REALMENTE RELEVANTES.

NÃO ABORDAR OBJETIVOS E
INFORMAÇÕES SECUNDÁRIAS QUE NÃO
SEJAM RELEVANTE

PARA O TRABALHO. MUITAS VEZES MENOS É MAIS.

# ORGANIZAÇÃO DA INFORMAÇÃO
# ASSERTIVIDADE

# DIRECIONAMENTO CLARO

INFORMAÇÕES QUE
SÃO
FUNDAMENTAIS:

Contexto

Objetivo do projeto
Target (Público-alvo)
Mercado / Concorrência
Budget (orçamento)
Prazo

Pontos de atenção

2023

MIAMI AD SCHOOL

BRIEFING & INSIGHT

BRIEFING & INSIGHT

MIAMI AD SCHOOL

2023

INFORMAÇÕES QUE
SÃO
FUNDAMENTAIS:

_CONTEXTO

Por que esse trabalho vai ser desenvolvido?

Um panorama geral sobre o que está acontecendo
e uma breve introdução do que vai ser explorado.

ex: “nos últimos anos a categoria se tornou extremamente
competitiva e com isso a imagem da marca vem perdendo
força como referência em inovação"

2023

MIAMI AD SCHOOL

BRIEFING & INSIGHT

BRIEFING & INSIGHT

MIAMI AD SCHOOL

2023

INFORMAÇÕES QUE
SÃO
FUNDAMENTAIS:

_OBJETIVO DO PROJETO

Qual é o principal desafio a ser resolvido?

Lançamento de produto
Fortalecimento de imagem
Posicionamento de marca
Reposicionamento de marca
Campanha institucional
Campanha de aquisição
Rejuvenescimento de marca
Jornada do consumidor

2023

MIAMI AD SCHOOL

BRIEFING & INSIGHT

BRIEFING & INSIGHT

MIAMI AD SCHOOL

2023

INFORMAÇÕES QUE
SÃO
FUNDAMENTAIS:

_TARGET (PÚBLICO-ALVO)

Com quem iremos nos conectar?

_Faixa etária

_Classe social

_Localização

_Hábitos de consumo

_Descrição atitudinal - muito importante

2023

MIAMI AD SCHOOL

BRIEFING & INSIGHT

BRIEFING & INSIGHT

MIAMI AD SCHOOL

2023

INFORMAÇÕES QUE
SÃO
FUNDAMENTAIS:

2023

MIAMI AD SCHOOL

BRIEFING & INSIGHT

_MERCADO / CONCORRÊNCIA

Em que mar navegamos? Existe algum ponto de atenção?

últimos movimentos de comunicação, posicionamento, iniciativas de marca e comunicação

_Cenário atual

_Fortalezas

_Fraquezas

_Principais movimentos

_Concorrentes diretos

BRIEFING & INSIGHT

MIAMI AD SCHOOL

2023

INFORMAÇÕES QUE
SÃO
FUNDAMENTAIS:

_BUDGET (ORÇAMENTO) E PRAZO

Qual é o nosso universo de execução?

_PONTOS DE ATENÇÃO

Existe alguma dica que vale ser ressaltada que
ajudará no projeto?

'''




# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
genai.configure(api_key=gemini_api_key)

# Inicializa o modelo Gemini
modelo_linguagem = genai.GenerativeModel("gemini-1.5-flash")  # Usando Gemini


# Função para limpar o estado do Streamlit
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Função principal da página de planejamento de mídias
def briefing():
    st.subheader('Contexto')
    st.text('''Aqui contextualizamos o momento do cliente e o escopo de atuação da Macfor.''')
    

    #Contexto
    nome_cliente = st.text_input('Nome do Cliente:', help="Digite o nome do cliente que será planejado. Ex: 'Empresa XYZ'")

    projeto_peca = st.text_input('Qual é o projeto ou peça?:', help="Apresente aqui, resumidamente, o serviço pelo qual o cliente contratou a Macfor para realizar.")

    cenario = st.text_input('Qual o cenário em que o cliente se encontra nesse momento?', help = "Apresentar todo o contexto da solicitação, seu histórico, o cenário a que se encontra que justifique e defenda o projeto.")

    objetivos = st.text_input('Quais são os objetivos do cliente ao contratar a Macfor?', help = "O que queremos alcançar, direta e indiretamente, tangível e intangível. Seja o projeto na totalidade, seja somente sob responsabilidades Macfor.")

    publico = st.text_input('Qual é o nosso público-alvo?', help = "Com quem devemos falar? Qual será nossa segmentação? Temos mailing?")

    periodo = st.text_input('Qual será o nosso período de atuação?', help = "Quando o projeto acontece? Qual período? Quando devemos começar a trabalhar? Quando será a entrega ou publicação do material?")

    verba = st.text_input('Qual será a verba disponível para a Macfor utilizar em sua atuação?', help = "Considerar valor total, que consiste em custos de produção, mídia e ergometria.")

    st.subheader('Criação')
    st.text('''Aqui criamos o documento que guia o processo criativo da Macfor.''')

    oque = st.text_input('O que vamos fazer?', help = "Detalhar quais peças vamos criar, tudo que deve contemplar em nosso plano, segundo expectativas da cliente + sugestão Macfor.")

    KV = st.text_input('Seguir orientação de KV? Qual deverá ser usado?', help = "Validar com o cliente o KV que devemos trabalhar a partir dos materiais da MAKE ou se vamos seguir com alguma referência fora do KV. Caso não tenha um KV, devemos seguir com fotografias, ilustrações? Qual a expectativa visual para essa peça?")

    mensagem = st.text_input('O que vamos dizer na comunicação?', help = "Alinhar as principais mensagens que devemos passar em nossas peças para o público em questão.")

    restricoes = st.text_input('Existe alguma referência, restrição, obrigatoriedade sobre uso de imagens, palavras e termos?', help = "Apresentar qualquer orientação que deve ser seguida.")

    redes = st.text_input('Quais redes sociais deverão ser usadas?', help = "Neste a definição virá em nosso Plano, mas o cliente pode ter algum desejo, recomendação, sugestão. Incluir peças e formatos após aprovação de volumetria. Incluir link da volumetria no Drive.")

    obs = st.text_input('Observações e comentários', help = "Use esse espaço para detalhar ou complementar alguma informação que você considere importante para o desenvolvimento do projeto.")
  

    pest_files = 1



  
    if pest_files is not None:
        if "relatorio_gerado" in st.session_state and st.session_state.relatorio_gerado:
            st.subheader("Briefing")
            for tarefa in st.session_state.resultados_tarefas:
                st.markdown(f"**Arquivo**: {tarefa['output_file']}")
                st.markdown(tarefa["output"])
            
            # Botão para limpar o estado
            if st.button("Gerar Briefing"):
                limpar_estado()
                st.experimental_rerun()
        else:
            if st.button('Gerar Briefing'):
                if not nome_cliente:
                    st.write("Por favor, preencha todas as informações do cliente.")
                else:
                    with st.spinner('Gerando o documento de briefing...'):





                            



                        prompt_context = f'''
                        Considerando as diretrizes para o desenvolvimento de um bom documetno de Briefing: ({oq_brief})
                        
                        Você é um gerente de projetos altamente qualificado com escrita concisa e impecável.

                        
                        
                        A empresa de Marketing Digital Macfor foi contratada pelo cliente {nome_cliente}.
                        
                        1. Qual é o projeto ou peça? (EX: Projeto Webinar Soja. Desenvolvimento de campanhas para promover o Webinar, atrair audiência e coletar leads qualificados.): {projeto_peca}.

                        2. Qual o cenário em que o cliente se encontra nesse momento? (Ex. O plantio da safra de soja terá início na segunda quinzena de Setembro, momento em que os produtores colocam todas suas energias sobre a lavoura para garantir o timing correto da cultura, uma vez que a janela de plantio é extremamente importante para o sucesso da cultura e também da safrinha.

Com isso, queremos oferecer um Webinar para estaremos com os produtores, mostrando que a Syngenta é a empresa da soja. Momentos antes da safra se iniciar, queremos oferecer um bate-papo informal de produtor para produtor onde nos colocamos do lado dele, discutindo assuntos propostos por eles, para a melhora do manejo e atingimento do potencial máximo da lavoura.
): {cenario}

                        3. Quais são os objetivos do cliente ao contratar a Macfor? (Queremos estreitar e fortalecer nossa relação com pequenos produtores de soja, abrindo canais de comunicação onde o próprio produtor exerce a fala, divide experiências, promove nossa marca.): {objetivos}

                        4. Público alvo: {publico}

                        5. Período: {periodo} (nessa etapa, escreva apenas o período.)

                        6. Verba: {verba} (nessa etapa, escreva apenas a verba. ex: R$ 50.000,00)

                        Redija um documento de Briefing onde cada etapa possui 2 parágrafos formalmente redigidos de uma forma que o documento possa ser usado como referência para
                        guiar as ações da Macfor ao longo do projeto. Gere cada etapa dentro de uma caixa.
                        
                        
                        '''
                        context_output = modelo_linguagem.generate_content(prompt_context).text


                        prompt_criacao = f'''
                        Considerando as diretrizes para o desenvolvimento de um bom documetno de Briefing: ({oq_brief})
                        
                        Você é um gerente de projetos altamente qualificado com escrita impecável.

                        Aqui criamos o documento que guia o processo criativo da Macfor.
                        
                        A empresa de Marketing Digital Macfor foi contratada pelo cliente {nome_cliente}.
                        
                        1. O que vamos fazer?: {oque}.

                        2. Seguir orientação de KV? Qual deverá ser usado?: {KV}

                        3. O que vamos dizer na comunicação? (Ex. Dar início a Jornada da Soja. Em nossos Webinars, disponibilizaremos conteúdos ricos para todas as etapas da cultura. Conteúdos nos quais serão oferecidos principalmente pelos próprios produtores, em parceria com a Syngenta. Será uma troca de experiências de produtor para produtor, onde os principais temas foram escolhidos por eles mesmos.): {mensagem}

                        4. Existe alguma referência, restrição, obrigatoriedade sobre uso de imagens, palavras e termos? (Ex. Precisamos aplicar o logo da CESB em todas as nossas peças de comunicação. Incluir link no Drive para as referências.): {restricoes}

                        5. Quais redes sociais deverão ser usadas?: {redes}

                        6. Observações e comentários: {obs}


                        Redija um documento de Briefing criativo onde cada etapa possui 2 parágrafos formalmente redigidos de uma forma que o documento possa ser usado como referência para
                        guiar as ações da Macfor ao longo do projeto. Gere cada etapa dentro de uma caixa.
                        
                        
                        '''
                        criacaot_output = modelo_linguagem.generate_content(prompt_criacao).text





                        #Printando Tarefas

                        st.header('1. Etapa Contextual')
                        st.markdown(context_output)

                        
                

                        st.header('2. Etapa Criativa')
                        st.markdown(criacaot_output)

                       

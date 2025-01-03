import os
import streamlit as st
from crewai import Agent, Task, Process, Crew
from langchain_openai import ChatOpenAI
from pymongo import MongoClient
from datetime import datetime
from crewai_tools import tool
from crewai_tools import PDFSearchTool, CSVSearchTool
from tavily import TavilyClient
import csv

def visualizar_planejamentos():
    # Consultar todos os documentos da coleção no MongoDB
    planejamentos = collection.find()  # Aqui estamos recuperando todos os documentos da coleção 'auto_doc'
    
    # Se não houver documentos
    if planejamentos.count() == 0:
        st.write("Nenhum planejamento encontrado.")
        return
    
    # Exibir os resultados no Streamlit
    st.subheader("Planejamentos Já Gerados")
    
    for planejamento in planejamentos:
        st.markdown(f"### Planejamento para: {planejamento.get('cliente')}")
        st.markdown(f"**Data de Criação:** {planejamento.get('timestamp')}")
        
        # Exibindo as informações dos campos de planejamento (como SWOT, GC, etc.)
        st.markdown(f"**SWOT:** {planejamento.get('SWOT')}")
        st.markdown(f"**GC:** {planejamento.get('GC')}")
        st.markdown(f"**Posicionamento de Marca:** {planejamento.get('Posicionamento_Marca')}")
        st.markdown(f"**Brand Persona:** {planejamento.get('Brand_Persona')}")
        st.markdown(f"**Buyer Persona:** {planejamento.get('Buyer_Persona')}")
        st.markdown(f"**Tom de Voz:** {planejamento.get('Tom_Voz')}")
        st.markdown(f"**PEST:** {planejamento.get('PEST')}")
        st.markdown(f"**Revisão:** {planejamento.get('Revisao')}")
        st.markdown(f"**Estratégia de Conteúdo:** {planejamento.get('Estrategia_Conteudo')}")
        st.markdown(f"**Plano SEO:** {planejamento.get('Plano_SEO')}")
        
        st.markdown("---")  # Separador visual entre os planejamentos



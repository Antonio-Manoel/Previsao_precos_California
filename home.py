#Importações

import geopandas as gpd
import numpy as np
import pandas as pd
import pydeck as pdk
import shapely
import streamlit as st

from joblib import load

from notebooks.apoio.config import DADOS_GEO_MEDIAN, DADOS_LIMPOS, MODELO_FINAL

# ===============
# Criação do app
# ===============

#Criação de uma função para ler os dados limpos
@st.cache_data
def dados_limpos():
    return pd.read_parquet(DADOS_LIMPOS)

#Criação de uma função para ler os dados geo median
def dados_geo_median():
    gdf_geo_median = gpd.read_parquet(DADOS_GEO_MEDIAN)
    # Explodir MultiPolígonos em polígonos individuais
    gdf_geo_median = gdf_geo_median.explode(ignore_index=True)
    
    # Função para verificar e corrigir geometrias inválidas
    def corrigir_geometrias(geometry):
        # Corrigir geometria inválida
        if not geometry.is_valid:
            geometry = geometry.buffer(0)
        # Oriente o polígono no sentido anti-horário se for um Polígono ou Multipolígono.
        if isinstance(
            geometry, (shapely.geometry.Polygon, shapely.geometry.MultiPolygon)
        ):
            geometry = shapely.geometry.polygon.orient(geometry, sign=10)

        return geometry
        
    # Aplicar a função de fixação e orientação às geometrias.
    gdf_geo_median["geometry"] = gdf_geo_median["geometry"].apply(corrigir_geometrias)
    
    # Função para extrair coordenadas poligonais
    def extrair_coords(geometry):
        return (
            [[[x, y] for x, y in geometry.exterior.coords]] 
            if isinstance(geometry, shapely.geometry.Polygon)
            else [
                [[x, y] for x, y in geometry.exterior.coords] 
                for polygon in geometry.geoms
            ]
        )
        
    # Aplique a conversão de coordenadas e armazene em uma nova coluna.
    gdf_geo_median["geometry"] = gdf_geo_median["geometry"].apply(extrair_coords)

    return gdf_geo_median

#Função para carregar o modelo final
@st.cache_resource
def modelo_final():
    return load(MODELO_FINAL)

#Crie variáveis para chamar cada função
DadosLimpos = dados_limpos()
DadosGeoMedian = dados_geo_median()
ModeloFinal = modelo_final()

#Crie o título do app
st.title("Previsão de Preços de Imóveis da Califórnia")

#Crie uma variável para ordenar os valores únicos de condados
condados = sorted(DadosGeoMedian["name"].unique())

#Defina 2 colunas para o app
coluna1, coluna2 = st.columns(2)

# =========================
# COLUNA 1 → INPUT DO USUÁRIO + PREVISÃO
# =========================
with coluna1:
    # Cria um formulário no Streamlit (evita atualização a cada input)
    with st.form(key="formulario"):
        # Selectbox para escolher o condado
        escolher_condado = st.selectbox("Condado", condados)
        
        # Pega longitude e latitude do condado selecionado
        longitude = DadosGeoMedian.query("name == @escolher_condado")["longitude"].values
        latitude = DadosGeoMedian.query("name == @escolher_condado")["latitude"].values
        
        # Input numérico para idade do imóvel
        housing_median_age = st.number_input("Idade do Imóvel", value=10 , min_value=1, max_value=50)

        # Pega variáveis do dataset com base no condado selecionado
        total_rooms = DadosGeoMedian.query("name == @escolher_condado")["total_rooms"].values
        total_bedrooms = DadosGeoMedian.query("name == @escolher_condado")["total_bedrooms"].values
        population = DadosGeoMedian.query("name == @escolher_condado")["population"].values
        households = DadosGeoMedian.query("name == @escolher_condado")["households"].values

        # Slider para renda média (em milhares de dólares)
        median_income = st.slider("Renda média (milhares de US$)", 5.0, 100.0, 45.0, 5.0)
        
        # Ajusta escala da renda (modelo espera valores menores)
        escala_renda = median_income/10
        
        # Pega categoria de proximidade do oceano
        ocean_proximity = DadosGeoMedian.query("name == @escolher_condado")["ocean_proximity"].values
        
        # Cria bins para categorizar renda (feature engineering)
        bins_income = [0, 1.5, 3, 4.5, 6, np.inf]
        
        # Converte renda contínua em categoria
        cat_escala_renda = np.digitize(escala_renda, bins=bins_income)


        








        
        
        # Features derivadas (já calculadas no dataset)
        
        # Monta dicionário com todas as variáveis de entrada do modelo
        
        # Converte entrada em DataFrame (formato esperado pelo modelo)
        
        # Botão para disparar a previsão
        
    # Quando o botão é clicado
        # Faz a previsão com o modelo treinado
    
        # Mostra o resultado formatado
        

# =========================
# COLUNA 2 → MAPA INTERATIVO
# =========================
    # Define o estado inicial do mapa (posição e zoom)

    # Camada com TODOS os condados (em azul)
    
    # Filtra o condado selecionado
    
    # Camada de destaque (condado selecionado em vermelho)
    
    # Tooltip (informação ao passar o mouse)
    
    # Cria o mapa com PyDeck

    # Renderiza o mapa no Streamlit
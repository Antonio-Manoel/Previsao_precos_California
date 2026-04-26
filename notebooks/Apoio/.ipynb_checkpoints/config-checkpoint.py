from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parents[2]

PASTA_DADOS = PASTA_PROJETO / "dados"

# coloque abaixo o caminho para os arquivos de dados de seu projeto
DADOS_ORIGINAIS = PASTA_DADOS / "housing.csv.zip"
DADOS_LIMPOS = PASTA_DADOS / "housing_clean.parquet"
DADOS_GEO_ORIGINAIS = PASTA_DADOS / "california_counties.geojson"
DADOS_GEO_MEDIAN = PASTA_DADOS / "gdf_counties.parquet"
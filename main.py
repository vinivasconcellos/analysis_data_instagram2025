import pandas as pd
import numpy as np
import os
import sys
sys.path.append("../src")
from limpeza_dados import converter_k, formatar_mes
from calculo_engajamento import calcular_engajamento
from medias import media_por_grupo
from medias_grupo import resumo_max_min_por_grupo
from categorias import categorizar_post
from outliers import detectar_outliers_iqr, sem_outliers_iqr
from gerar_relatorio_mensal import gerar_relatorios_mensais
from gerar_pdf import gerar_pdf_resumo, gerar_pdf_com_e_sem_outliers

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "Posts_2025.xlsx")
df_postagens2025 = pd.read_excel(csv_path)

#tratamento
colunas = ["Curtidas", "Coment.", "Compart.", "Salvos", "Visualiz.", "Alcance", "Visitas", "Seguid."]
for col in colunas:
    df_postagens2025[col] = df_postagens2025[col].apply(converter_k)

print(df_postagens2025)


df_postagens2025 = formatar_mes(df_postagens2025)
print(df_postagens2025.head())
print(df_postagens2025.info())

################
print(df_postagens2025)
#filtragem
colunas = ["Curtidas", "Coment.", "Compart.", "Salvos", "Visualiz.", "Alcance", "Visitas", "Seguid.", "Engajamento"]

#cálculo engajamento:
df_postagens2025 = calcular_engajamento(df_postagens2025)
print(df_postagens2025)

#médias
df_medias = media_por_grupo(df_postagens2025, colunas)
print(df_medias.round(2))

#qual formato teve o maior e o menor valor médio de acordo com a métrica
df_resumo = resumo_max_min_por_grupo(df_postagens2025, colunas, grupo="Formato")
print(df_resumo.round(2))

###############
#categorias

df_postagens2025["Categoria"] = df_postagens2025["Título / Tema do Post"].map(categorizar_post)
print(df_postagens2025)
df_postagens2025.to_excel("postagens_categorizadas_2025.xlsx", index=False)
#####################
#outliers

#Detectar outliers de engajamento
outliers_eng = detectar_outliers_iqr(df_postagens2025, coluna="Engajamento")
print("Outliers de Engajamento:")
print(outliers_eng)

#Top categorias presentes nos outliers
top_categorias_outliers_eng = (outliers_eng["Categoria"].value_counts().reset_index())
top_categorias_outliers_eng.columns = ["Categoria", "Qtd_Outliers"]
print(top_categorias_outliers_eng)
#####################
#métricas sem outliers
# quais formatos tiveram melhor engajamento por categoria retirando os outliers

df_analise_categoria_tema_eng_s = sem_outliers_iqr(df_postagens2025, coluna="Engajamento")
print(df_analise_categoria_tema_eng_s)

# quais formatos tiveram melhor engajamento por categoria com outlier
analise_categoria_tema_eng = df_postagens2025[["Formato", "Categoria", "Engajamento"]].groupby(["Categoria", "Formato"]).mean().round(2).sort_values(by=["Categoria", "Engajamento"], ascending=[True, False])
#print(analise_categoria_tema_eng)

# quais formatos tiveram melhor engajamento por categoria sem outlier
analise_categoria_tema_eng_s = df_analise_categoria_tema_eng_s[["Formato", "Categoria", "Engajamento"]].groupby(["Categoria", "Formato"]).mean().round(2).sort_values(by=["Categoria", "Engajamento"], ascending=[True, False])
#print(analise_categoria_tema_eng_s)

# mostrando os dois resultados para comparação
analise_categoria_tema_eng_s = analise_categoria_tema_eng_s.rename(columns={"Engajamento": "Eng_Sem_Outliers"})
analise_categoria_tema_eng = analise_categoria_tema_eng.rename(columns={"Engajamento": "Eng_Com_Outliers"})
df_cat_eng_s_c = analise_categoria_tema_eng.merge(analise_categoria_tema_eng_s, on=["Categoria", "Formato"], how="outer")
df_cat_eng_s_c = df_cat_eng_s_c.fillna(0)

print(df_cat_eng_s_c.sort_values(by=["Categoria", "Eng_Sem_Outliers"], ascending=[True, False]))

# Média de engajamento por categoria sem outliers
df_media_eng_cat_s = df_analise_categoria_tema_eng_s[["Categoria", "Engajamento"]].groupby(["Categoria"]).mean()
df_media_eng_cat_s = df_analise_categoria_tema_eng_s[["Categoria", "Engajamento"]].groupby(["Categoria"]).mean().sort_values(by=["Engajamento", "Categoria"], ascending=[False, True])
df_media_eng_cat_s = df_media_eng_cat_s.reset_index()
df_media_eng_cat_s.columns = ["Categoria", "Media_Eng_Sem_Outliers"]

# Média de engajamento por categoria com outliers
df_media_eng_cat = df_postagens2025[["Categoria", "Engajamento"]].groupby(["Categoria"]).mean()
df_media_eng_cat = df_postagens2025[["Categoria", "Engajamento"]].groupby(["Categoria"]).mean().sort_values(by=["Engajamento", "Categoria"], ascending=[False, True])
df_media_eng_cat = df_media_eng_cat.reset_index()
df_media_eng_cat.columns = ["Categoria", "Media_Eng_Com_Outliers"]

#df_com = df_media_eng_cat.rename(columns={"Engajamento": "Eng_Com_Outliers"})


df_tot = df_media_eng_cat.merge(df_media_eng_cat_s, on=["Categoria"], how="outer")
df_tot = df_tot.fillna(0)
df_tot = df_tot.sort_values(by="Media_Eng_Sem_Outliers", ascending=False)
print("Ordem decrescente de engajamento sem outliers:")
print(df_tot.round(2))
df_tot = df_tot.sort_values(by="Media_Eng_Com_Outliers", ascending=False)
print("Ordem decrescente de engajamento com outliers:")
print(df_tot.round(2))
####################
# gerar relatórios mensais

gerar_relatorios_mensais(df_postagens2025)
gerar_pdf_resumo(df_postagens2025)
gerar_pdf_com_e_sem_outliers(df_postagens2025)
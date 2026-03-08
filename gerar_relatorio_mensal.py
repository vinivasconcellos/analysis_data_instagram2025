import os
import pandas as pd
from datetime import date
from medias import media_por_grupo
from medias_grupo import resumo_max_min_por_grupo
from outliers import detectar_outliers_iqr
from limpeza_dados import extrair_ano_mes
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def gerar_relatorios_mensais(df_postagens2025, pasta_saida="outputs/relatorios_mensais"):

    pasta_saida = os.path.join(BASE_DIR, pasta_saida)
    os.makedirs(pasta_saida, exist_ok=True)

    meses = df_postagens2025["Mês"].unique()
    # 1. Pega a data de hoje
    data_atual = date.today().year

    # 2. Subtrai 1 do ano atual
    ano_anterior = data_atual - 1

    for referencia in meses:
        mes = extrair_ano_mes(referencia)
        df_mes = df_postagens2025[df_postagens2025["Mês"] == referencia]
        colunas = [
            "Curtidas","Coment.","Compart.","Salvos",
            "Visualiz.","Alcance","Visitas","Seguid.","Engajamento"]

        # médias
        df_medias = media_por_grupo(df_mes, colunas)

        # resumo
        df_resumo = resumo_max_min_por_grupo(df_mes, colunas, grupo="Formato")

        # outliers
        df_outliers = detectar_outliers_iqr(df_mes, coluna="Engajamento")

        caminho = os.path.join(pasta_saida, f"relatorio_{mes}_{ano_anterior}.xlsx")

        with pd.ExcelWriter(caminho) as writer:

            df_mes.to_excel(writer, sheet_name="dados_mes", index=False)

            df_medias.to_excel(writer, sheet_name="medias")

            df_resumo.to_excel(writer, sheet_name="resumo")

            df_outliers.to_excel(writer, sheet_name="outliers")

        print(f"Relatório gerado: {caminho}")
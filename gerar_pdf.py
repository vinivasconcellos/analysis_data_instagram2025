import os
import numpy as np
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from outliers import sem_outliers_iqr

def gerar_insights_automaticos(df_tot):

    top_categoria = df_tot.iloc[0]["Categoria"]
    top_eng = df_tot.iloc[0]["Media_Eng_Sem_Outliers"]
    idx_max_impacto = df_tot["Dif_Percentual_Outliers"].idxmax()
    cat_mais_afetada = df_tot.loc[idx_max_impacto, "Categoria"]
    impacto_max = df_tot.loc[idx_max_impacto, "Dif_Percentual_Outliers"]
    impacto_medio = df_tot["Dif_Percentual_Outliers"].mean()
    top3 = df_tot.head(3)
    insights = []
    insights.append(
        f"A categoria com maior engajamento sem outliers é {top_categoria} ({top_eng:.2f}).")

    insights.append(
        f"A categoria mais afetada por outliers é {cat_mais_afetada}, com impacto de {impacto_max:.1f}%.")

    insights.append(
        f"O impacto médio dos outliers nas categorias é de {impacto_medio:.1f}%.")
    
    insights.append(
        f"Top 3 categorias por engajamento (sem outliers):")
    
    for i, row in top3.reset_index(drop=True).iterrows():
        insights.append(f"{i+1}º {row['Categoria']} - {row['Media_Eng_Sem_Outliers']:.2f}")
      
    return insights

def gerar_pdf_resumo(df_postagens2025):
    
    os.makedirs("outputs/relatorios_pdf", exist_ok=True)

    caminho_pdf = "outputs/relatorios_pdf/resumo_geral_comparacao_com_e_sem_outliers.pdf"

    # média engajamento por categoria sem outliers
    df_analise_categoria_tema_eng_s = sem_outliers_iqr(df_postagens2025, coluna="Engajamento")
    df_media_eng_cat_s = (df_analise_categoria_tema_eng_s[["Categoria", "Engajamento"]].groupby("Categoria").mean().reset_index())
    
    df_media_eng_cat_s.columns = ["Categoria", "Media_Eng_Sem_Outliers"]

    # média engajamento com outliers
    df_media_eng_cat = (df_postagens2025[["Categoria", "Engajamento"]].groupby("Categoria").mean().reset_index())

    df_media_eng_cat.columns = ["Categoria", "Media_Eng_Com_Outliers"]

    # juntar os dois
    df_tot = df_media_eng_cat.merge(df_media_eng_cat_s, on=["Categoria"], how="outer")
    #df_tot = df_media_eng_cat.merge(df_media_eng_cat_s, on="Categoria", how="outer")

    df_tot = df_tot.fillna(0)

    # ordenar por engajamento sem outliers
    df_tot = df_tot.sort_values(by="Media_Eng_Sem_Outliers", ascending=False)

    #cálculo diferença percentual com e sem outliers
    df_tot["Dif_Percentual_Outliers"] = (
    (df_tot["Media_Eng_Com_Outliers"] - df_tot["Media_Eng_Sem_Outliers"])
    / df_tot["Media_Eng_Sem_Outliers"]) * 100

    insights = gerar_insights_automaticos(df_tot)
   
    # gráfico
    plt.figure(figsize=(10,6))

    categorias = df_tot["Categoria"]

    x = np.arange(len(categorias))

    largura = 0.35

    #barras1 = plt.bar(
    plt.bar(    
    x - largura/2,
    df_tot["Media_Eng_Com_Outliers"],
    largura,
    color="#9aa0a6",
    label="Com Outliers")
    #plt.bar_label(barras1, fmt="%.2f", padding=3)

    #barras2 = plt.bar(
    plt.bar(    
    x + largura/2,
    df_tot["Media_Eng_Sem_Outliers"],
    largura,
    color="#2ecc71",
    label="Sem Outliers")
    #plt.bar_label(barras2, fmt="%.2f", padding=3)

    #cálculo diferença percentual com e sem outliers
    for i, v in enumerate(df_tot["Dif_Percentual_Outliers"]):
        plt.text(
            x[i],
            max(df_tot["Media_Eng_Com_Outliers"].iloc[i],
                df_tot["Media_Eng_Sem_Outliers"].iloc[i]) + 0.3,
            f"{v:.1f}%",
            ha="center",
            fontsize=9,
            color="black"
        )


    plt.xticks(x, categorias, rotation=90)

    plt.ylabel("Engajamento Médio")

    plt.title("Comparação de Engajamento por Categoria")

    plt.legend()

    plt.tight_layout()
    plt.grid(axis="y", linestyle="--", alpha=0.3)

    caminho_grafico = "outputs/relatorios_pdf/grafico_comparacao_engajamento.png"

    plt.savefig(caminho_grafico)

    # criar PDF
    c = canvas.Canvas(caminho_pdf)

    c.drawString(100, 800, "Relatório de Engajamento Instagram")

    c.drawString(100, 780, "Comparação com e sem outliers")

    c.drawImage(caminho_grafico, 50, 350, width=500, height=350)

    c.showPage()

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "Resumo Analítico")    
    
    c.setFont("Helvetica", 12)

    y = 750

    for texto in insights:

        c.drawString(10, y, texto)

        y -= 30
    
    c.save()

    print("PDF comparativo gerado com sucesso!")

def gerar_pdf_com_e_sem_outliers(df_postagens2025):
    
    os.makedirs("outputs/relatorios_pdf", exist_ok=True)

    caminho_pdf = "outputs/relatorios_pdf/resumo_geral_dois_graficos.pdf"

    # média engajamento por categoria sem outliers
    df_analise_categoria_tema_eng_s = sem_outliers_iqr(df_postagens2025, coluna="Engajamento")
    df_media_eng_cat_s = (df_analise_categoria_tema_eng_s[["Categoria", "Engajamento"]].groupby("Categoria").mean().reset_index())
    
    df_media_eng_cat_s.columns = ["Categoria", "Media_Eng_Sem_Outliers"]

    # média engajamento com outliers
    df_media_eng_cat = (df_postagens2025[["Categoria", "Engajamento"]].groupby("Categoria").mean().reset_index())

    df_media_eng_cat.columns = ["Categoria", "Media_Eng_Com_Outliers"]

    # juntar os dois
    df_tot = df_media_eng_cat.merge(df_media_eng_cat_s, on=["Categoria"], how="outer")
    #df_tot = df_media_eng_cat.merge(df_media_eng_cat_s, on="Categoria", how="outer")

    df_tot = df_tot.fillna(0)

    # ordenar por engajamento sem outliers
    df_tot = df_tot.sort_values(by="Media_Eng_Sem_Outliers", ascending=False)

    # gráfico
    categorias = df_tot["Categoria"]

    x = np.arange(len(categorias))

    fig, axs = plt.subplots(2, 1, figsize=(10,10))

    # -------------------------
    # gráfico 1 (com outliers)
    # -------------------------
    
    barras1 = axs[0].bar(x, df_tot["Media_Eng_Com_Outliers"], color="#9aa0a6")
    axs[0].set_title("Engajamento Médio por Categoria (Com Outliers)")
    axs[0].set_ylabel("Engajamento")
    axs[0].set_xticks(x)
    axs[0].set_xticklabels(categorias, rotation=90)
    axs[0].bar_label(barras1, fmt="%.2f")
    # -------------------------
    # gráfico 2 (sem outliers)
    # -------------------------

    barras2 = axs[1].bar(x, df_tot["Media_Eng_Sem_Outliers"], color="#2ecc71")
    axs[1].set_title("Engajamento Médio por Categoria (Sem Outliers)")
    axs[1].set_ylabel("Engajamento")
    axs[1].set_xticks(x)
    axs[1].set_xticklabels(categorias, rotation=90)
    axs[1].bar_label(barras2, fmt="%.2f")

    plt.tight_layout()
    barras1 = plt.grid(axis="y", linestyle="--", alpha=0.3)
    barras2 = plt.grid(axis="y", linestyle="--", alpha=0.3)

    caminho_grafico = "outputs/relatorios_pdf/grafico_dois_graficos_engajamento.png"

    plt.savefig(caminho_grafico)

    # criar PDF
    c = canvas.Canvas(caminho_pdf)

    c.drawString(100, 800, "Relatório de Engajamento Instagram")

    c.drawString(100, 780, "Comparação com e sem outliers")

    c.drawImage(caminho_grafico, 50, 350, width=500, height=350)

    c.save()

    print("PDF com dois gráficos gerado com sucesso!")   



######################

# import os
# import numpy as np
# import matplotlib.pyplot as plt
# from reportlab.pdfgen import canvas
# from outliers import sem_outliers_iqr

# def gerar_pdf_resumo(df_postagens2025):
    
#     os.makedirs("outputs/relatorios_pdf", exist_ok=True)

#     caminho_pdf = "outputs/relatorios_pdf/resumo_geral_comparacao_com_e_sem_outliers.pdf"

#     # média engajamento por categoria sem outliers
#     df_analise_categoria_tema_eng_s = sem_outliers_iqr(df_postagens2025, coluna="Engajamento")
#     df_media_eng_cat_s = (df_analise_categoria_tema_eng_s[["Categoria", "Engajamento"]].groupby("Categoria").mean().reset_index())
    
#     df_media_eng_cat_s.columns = ["Categoria", "Media_Eng_Sem_Outliers"]

#     # média engajamento com outliers
#     df_media_eng_cat = (df_postagens2025[["Categoria", "Engajamento"]].groupby("Categoria").mean().reset_index())

#     df_media_eng_cat.columns = ["Categoria", "Media_Eng_Com_Outliers"]

#     # juntar os dois
#     df_tot = df_media_eng_cat.merge(df_media_eng_cat_s, on=["Categoria"], how="outer")
#     #df_tot = df_media_eng_cat.merge(df_media_eng_cat_s, on="Categoria", how="outer")

#     df_tot = df_tot.fillna(0)

#     # ordenar por engajamento sem outliers
#     df_tot = df_tot.sort_values(by="Media_Eng_Sem_Outliers", ascending=False)

#     #cálculo diferença percentual com e sem outliers
#     df_tot["Dif_Percentual_Outliers"] = (
#     (df_tot["Media_Eng_Com_Outliers"] - df_tot["Media_Eng_Sem_Outliers"])
#     / df_tot["Media_Eng_Sem_Outliers"]) * 100

#     # categoria com maior engajamento sem outliers
#     top_categoria = df_tot.iloc[0]["Categoria"]
#     top_eng = df_tot.iloc[0]["Media_Eng_Sem_Outliers"]

#     # categoria mais afetada por outliers
#     idx_max_impacto = df_tot["Dif_Percentual_Outliers"].idxmax()

#     cat_mais_afetada = df_tot.loc[idx_max_impacto, "Categoria"]
#     impacto_max = df_tot.loc[idx_max_impacto, "Dif_Percentual_Outliers"]

#     # impacto médio dos outliers
#     impacto_medio = df_tot["Dif_Percentual_Outliers"].mean()

#     # top 3 categorias
#     top3 = df_tot.head(3)[["Categoria", "Media_Eng_Sem_Outliers"]]

#     # gráfico
#     plt.figure(figsize=(10,6))

#     categorias = df_tot["Categoria"]

#     x = np.arange(len(categorias))

#     largura = 0.35

#     #barras1 = plt.bar(
#     plt.bar(    
#     x - largura/2,
#     df_tot["Media_Eng_Com_Outliers"],
#     largura,
#     color="#9aa0a6",
#     label="Com Outliers")
#     #plt.bar_label(barras1, fmt="%.2f", padding=3)

#     #barras2 = plt.bar(
#     plt.bar(    
#     x + largura/2,
#     df_tot["Media_Eng_Sem_Outliers"],
#     largura,
#     color="#2ecc71",
#     label="Sem Outliers")
#     #plt.bar_label(barras2, fmt="%.2f", padding=3)

#     #cálculo diferença percentual com e sem outliers
#     for i, v in enumerate(df_tot["Dif_Percentual_Outliers"]):
#         plt.text(
#             x[i],
#             max(df_tot["Media_Eng_Com_Outliers"].iloc[i],
#                 df_tot["Media_Eng_Sem_Outliers"].iloc[i]) + 0.3,
#             f"{v:.1f}%",
#             ha="center",
#             fontsize=9,
#             color="black"
#         )


#     plt.xticks(x, categorias, rotation=90)

#     plt.ylabel("Engajamento Médio")

#     plt.title("Comparação de Engajamento por Categoria")

#     plt.legend()

#     plt.tight_layout()
#     plt.grid(axis="y", linestyle="--", alpha=0.3)

#     caminho_grafico = "outputs/relatorios_pdf/grafico_comparacao_engajamento.png"

#     plt.savefig(caminho_grafico)

#     # criar PDF
#     c = canvas.Canvas(caminho_pdf)

#     c.drawString(100, 800, "Relatório de Engajamento Instagram")

#     c.drawString(100, 780, "Comparação com e sem outliers")

#     c.drawImage(caminho_grafico, 50, 350, width=500, height=350)

#     # nova página com a diferença percentual
#     c.showPage()

#     c.setFont("Helvetica-Bold", 16)
#     c.drawString(100, 800, "Resumo Analítico")

#     c.setFont("Helvetica", 12)

#     c.drawString(100, 750, f"Categoria com maior engajamento (sem outliers): {top_categoria}")
#     c.drawString(100, 730, f"Engajamento médio: {top_eng:.2f}")

#     c.drawString(100, 690, f"Categoria mais afetada por outliers: {cat_mais_afetada}")
#     c.drawString(100, 670, f"Impacto dos outliers: {impacto_max:.1f}%")

#     c.drawString(100, 630, f"Impacto médio dos outliers nas categorias: {impacto_medio:.1f}%")

#     # top 3 categorias
#     c.drawString(100, 580, "Top 3 categorias por engajamento (sem outliers):")

#     y = 550

#     for i, row in top3.iterrows():

#         texto = f"{row['Categoria']} - {row['Media_Eng_Sem_Outliers']:.2f}"

#         c.drawString(120, y, texto)

#         y -= 25

#     c.save()

#     print("PDF comparativo gerado com sucesso!")

# def gerar_pdf_com_e_sem_outliers(df_postagens2025):
    
#     os.makedirs("outputs/relatorios_pdf", exist_ok=True)

#     caminho_pdf = "outputs/relatorios_pdf/resumo_geral_dois_graficos.pdf"

#     # média engajamento por categoria sem outliers
#     df_analise_categoria_tema_eng_s = sem_outliers_iqr(df_postagens2025, coluna="Engajamento")
#     df_media_eng_cat_s = (df_analise_categoria_tema_eng_s[["Categoria", "Engajamento"]].groupby("Categoria").mean().reset_index())
    
#     df_media_eng_cat_s.columns = ["Categoria", "Media_Eng_Sem_Outliers"]

#     # média engajamento com outliers
#     df_media_eng_cat = (df_postagens2025[["Categoria", "Engajamento"]].groupby("Categoria").mean().reset_index())

#     df_media_eng_cat.columns = ["Categoria", "Media_Eng_Com_Outliers"]

#     # juntar os dois
#     df_tot = df_media_eng_cat.merge(df_media_eng_cat_s, on=["Categoria"], how="outer")
#     #df_tot = df_media_eng_cat.merge(df_media_eng_cat_s, on="Categoria", how="outer")

#     df_tot = df_tot.fillna(0)

#     # ordenar por engajamento sem outliers
#     df_tot = df_tot.sort_values(by="Media_Eng_Sem_Outliers", ascending=False)

#     # gráfico
#     categorias = df_tot["Categoria"]

#     x = np.arange(len(categorias))

#     fig, axs = plt.subplots(2, 1, figsize=(10,10))

#     # -------------------------
#     # gráfico 1 (com outliers)
#     # -------------------------
    
#     barras1 = axs[0].bar(x, df_tot["Media_Eng_Com_Outliers"], color="#9aa0a6")
#     axs[0].set_title("Engajamento Médio por Categoria (Com Outliers)")
#     axs[0].set_ylabel("Engajamento")
#     axs[0].set_xticks(x)
#     axs[0].set_xticklabels(categorias, rotation=90)
#     axs[0].bar_label(barras1, fmt="%.2f")
#     # -------------------------
#     # gráfico 2 (sem outliers)
#     # -------------------------

#     barras2 = axs[1].bar(x, df_tot["Media_Eng_Sem_Outliers"], color="#2ecc71")
#     axs[1].set_title("Engajamento Médio por Categoria (Sem Outliers)")
#     axs[1].set_ylabel("Engajamento")
#     axs[1].set_xticks(x)
#     axs[1].set_xticklabels(categorias, rotation=90)
#     axs[1].bar_label(barras2, fmt="%.2f")

#     plt.tight_layout()
#     barras1 = plt.grid(axis="y", linestyle="--", alpha=0.3)
#     barras2 = plt.grid(axis="y", linestyle="--", alpha=0.3)

#     caminho_grafico = "outputs/relatorios_pdf/grafico_dois_graficos_engajamento.png"

#     plt.savefig(caminho_grafico)

#     # criar PDF
#     c = canvas.Canvas(caminho_pdf)

#     c.drawString(100, 800, "Relatório de Engajamento Instagram")

#     c.drawString(100, 780, "Comparação com e sem outliers")

#     c.drawImage(caminho_grafico, 50, 350, width=500, height=350)

#     c.save()

#     print("PDF com dois gráficos gerado com sucesso!")    
def converter_k(valor):
    if isinstance(valor, str):
        if valor == "-" or valor == "":
            return 0
        valor = valor.strip().lower()
        if valor.endswith("k"):
            return int(float(valor.replace("k", "")) * 1000)
        elif valor.endswith("m"):
            return int(float(valor.replace("m", "")) * 1000000)
    return int(valor)

def formatar_mes(df_postagens2025):
    """
    Remove espaços extras da coluna 'Mês'
    """
    df_postagens2025 = df_postagens2025.copy()  # boa prática para evitar efeitos colaterais
    #df_postagens2025["Mês"] = df_postagens2025["Mês"].astype(str).str.strip()
    df_postagens2025["Mês"] = df_postagens2025["Mês"].str.strip()
    df_postagens2025["Título / Tema do Post"] = df_postagens2025["Título / Tema do Post"].str.strip()
    df_postagens2025["Formato"] = df_postagens2025["Formato"].str.strip()
    df_postagens2025["Mês"] = df_postagens2025["Mês"].str.capitalize()
    df_postagens2025["Título / Tema do Post"] = df_postagens2025["Título / Tema do Post"].str.lower()
    df_postagens2025["Formato"] = df_postagens2025["Formato"].str.capitalize()
    return df_postagens2025

def extrair_ano_mes(referencia):
    """
    Converte 'Jan' → '01'
    """

    mapa_meses = {
        "Jan": "01",
        "Fev": "02",
        "Mar": "03",
        "Abr": "04",
        "Mai": "05",
        "Jun": "06",
        "Jul": "07",
        "Ago": "08",
        "Set": "09",
        "Out": "10",
        "Nov": "11",
        "Dez": "12"
    }

    nome_mes = referencia
    mes = mapa_meses[nome_mes]

    return mes

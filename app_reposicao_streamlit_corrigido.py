import streamlit as st
import pandas as pd
import zipfile
import io

st.set_page_config(page_title="Dashboard Drawback", layout="wide")

st.title("Dashboard de Reposição - Drawback")

uploaded = st.file_uploader(
    "Enviar arquivo CSV ou ZIP exportado do Drawback",
    type=["csv", "zip"]
)

def ler_csv_drawback(file_bytes):
    linhas = file_bytes.decode("latin1").splitlines()

    header = linhas[0].replace(";;", "")
    colunas = header.split("|")

    dados = []

    for linha in linhas[1:]:
        linha = linha.strip()

        if not linha:
            continue

        linha = linha.replace(";;", "")
        linha = linha.strip('"')

        partes = linha.split("|")

        if len(partes) < len(colunas):
            partes += [""] * (len(colunas) - len(partes))

        dados.append(partes[:len(colunas)])

    df = pd.DataFrame(dados, columns=colunas)

    campos_numericos = [
        "QUANTIDADE_AUTORIZADA",
        "QUANTIDADE_REALIZADA",
        "VALOR_AUTORIZADO",
        "VALOR_REALIZADO"
    ]

    for campo in campos_numericos:
        if campo in df.columns:
            df[campo] = (
                df[campo]
                .astype(str)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
            )

            df[campo] = pd.to_numeric(df[campo], errors="coerce").fillna(0)

    return df

if uploaded:

    if uploaded.name.lower().endswith(".zip"):

        with zipfile.ZipFile(uploaded) as z:

            csv_name = [n for n in z.namelist() if n.lower().endswith(".csv")][0]

            with z.open(csv_name) as f:
                content = f.read()

            df = ler_csv_drawback(content)

    else:
        content = uploaded.read()
        df = ler_csv_drawback(content)

    df["QTDE_SALDO_DBK"] = (
        df["QUANTIDADE_AUTORIZADA"] - df["QUANTIDADE_REALIZADA"]
    )

    df["VALOR_SALDO_DBK"] = (
        df["VALOR_AUTORIZADO"] - df["VALOR_REALIZADO"]
    )

    total_itens = len(df)
    total_qtd_aut = df["QUANTIDADE_AUTORIZADA"].sum()
    total_saldo = df["QTDE_SALDO_DBK"].sum()
    total_valor = df["VALOR_AUTORIZADO"].sum()
    total_valor_saldo = df["VALOR_SALDO_DBK"].sum()

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Itens", total_itens)
    c2.metric("Qtde. Autorizada", f"{total_qtd_aut:,.2f}")
    c3.metric("Qtde. Saldo DBK", f"{total_saldo:,.2f}")
    c4.metric("Valor Autorizado", f"US$ {total_valor:,.2f}")
    c5.metric("Valor Saldo DBK", f"US$ {total_valor_saldo:,.2f}")

    st.divider()

    busca = st.text_input("Buscar por NCM, item ou descrição")

    if busca:
        filtro = (
            df["NCM"].astype(str).str.contains(busca, case=False, na=False)
            |
            df["DESCRICAO_COMPLEMENTAR_AUTORIZADA"].astype(str).str.contains(busca, case=False, na=False)
        )

        df = df[filtro]

    st.dataframe(
        df[
            [
                "NCM",
                "NUMERO_ITEM_REPOSICAO",
                "DESCRICAO_COMPLEMENTAR_AUTORIZADA",
                "QUANTIDADE_AUTORIZADA",
                "QUANTIDADE_REALIZADA",
                "QTDE_SALDO_DBK",
                "VALOR_AUTORIZADO",
                "VALOR_REALIZADO",
                "VALOR_SALDO_DBK"
            ]
        ],
        use_container_width=True,
        height=700
    )

else:
    st.info("Envie o CSV ou ZIP exportado do sistema Drawback.")

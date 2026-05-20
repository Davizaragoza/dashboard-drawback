import io
import zipfile
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="3S Corp | Reposição Drawback",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

LOGO_3S_BASE64 = "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"

PASTA_DADOS = Path("/tmp/dashboard_drawback_3s")
PASTA_DADOS.mkdir(parents=True, exist_ok=True)
ARQUIVO_ATUAL = PASTA_DADOS / "ultimo_arquivo.bin"
ARQUIVO_NOME = PASTA_DADOS / "ultimo_nome.txt"
ARQUIVO_DATA = PASTA_DADOS / "ultima_atualizacao.txt"

DADOS_AC = {
    "numero_ac": "250007916",
    "tipo": "Comum",
    "situacao": "Deferido pelo Sistema",
    "beneficiario": "02.921.346/0001-58",
    "razao_social": "ANJO QUÍMICA DO BRASIL LTDA",
    "valor_total_importacao": "1.661.297,68",
    "valor_total_mi": "32.267,51",
    "valor_total_exportacao_fob": "7.623.565,74",
    "valor_total_reposicao": "1.698.355,47",
    "vigencia": "24/06/2025 a 24/06/2027",
}

st.markdown(
    """
<style>
    .stApp {
        background: radial-gradient(circle at top left, #17212c 0%, #0a1018 40%, #060a0f 100%);
        color: #f8fafc;
    }

    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0f16 0%, #111923 100%);
        border-right: 1px solid rgba(255,255,255,.08);
    }
    [data-testid="stSidebar"] * { color: #f8fafc; }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }

    .top-header {
        display: grid;
        grid-template-columns: minmax(190px, 260px) minmax(280px, 1fr) repeat(3, minmax(230px, 1fr));
        gap: 14px;
        align-items: stretch;
        margin-bottom: 16px;
        width: 100%;
    }

    .brand-box {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        min-height: 94px;
        border-right: 1px solid rgba(220, 20, 60, .45);
        padding-right: 12px;
        overflow: hidden;
    }

    .brand-box img {
        width: 210px;
        max-width: 95%;
        object-fit: contain;
        display: block;
    }

    .title-box {
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 94px;
        min-width: 260px;
        overflow: hidden;
        border-right: 1px solid rgba(220, 20, 60, .35);
        padding-right: 14px;
    }

    .title-box h1 {
        margin: 0;
        font-size: clamp(25px, 2.1vw, 34px);
        color: #e71d3c;
        letter-spacing: .5px;
        white-space: nowrap;
        line-height: 1.1;
    }

    .title-box p {
        margin: 8px 0 0 0;
        font-size: clamp(13px, 1vw, 17px);
        color: #f1f5f9;
        white-space: normal;
        line-height: 1.3;
    }

    .header-card {
        border: 1px solid rgba(255,255,255,.12);
        background: linear-gradient(145deg, rgba(15,23,32,.95), rgba(9,14,20,.95));
        border-radius: 10px;
        padding: 16px 18px;
        box-shadow: 0 10px 30px rgba(0,0,0,.25);
        min-height: 94px;
        overflow-wrap: anywhere;
    }

    .header-label {
        font-size: 13px;
        color: #e2e8f0;
        text-transform: uppercase;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .header-value {
        font-size: 15px;
        color: #ffffff;
        font-weight: 800;
        margin-bottom: 7px;
        line-height: 1.3;
    }

    .header-sub {
        font-size: 12px;
        color: #cbd5e1;
        line-height: 1.4;
    }

    .ac-box {
        border: 1px solid rgba(255,255,255,.12);
        background: linear-gradient(145deg, rgba(18,27,37,.92), rgba(10,16,23,.92));
        border-radius: 10px;
        padding: 18px 20px 14px 20px;
        margin-bottom: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,.2);
    }

    .ac-title {
        color: #ff8c00;
        font-size: 18px;
        font-weight: 800;
        text-transform: uppercase;
        border-bottom: 1px solid rgba(255,140,0,.65);
        padding-bottom: 9px;
        margin-bottom: 14px;
    }

    .ac-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(360px, 1fr));
        gap: 22px;
    }

    .ac-row {
        display: grid;
        grid-template-columns: minmax(150px, 210px) minmax(180px, 1fr);
        border-bottom: 1px solid rgba(255,255,255,.08);
        min-height: 37px;
        align-items: center;
    }

    .ac-key {
        color: #f8fafc;
        font-size: 13px;
        border-right: 1px solid rgba(255,140,0,.7);
        padding-right: 8px;
        text-align: right;
    }

    .ac-val {
        color: #f8fafc;
        font-size: 14px;
        padding-left: 10px;
        overflow-wrap: anywhere;
    }

    .metric-card {
        border-radius: 10px;
        padding: 17px 18px;
        min-height: 122px;
        border: 1px solid rgba(255,255,255,.12);
        background: linear-gradient(145deg, rgba(18,27,37,.92), rgba(10,16,23,.95));
        box-shadow: 0 10px 30px rgba(0,0,0,.2);
    }

    .metric-cyan { border-color: rgba(34,211,238,.45); }
    .metric-green { border-color: rgba(34,197,94,.45); }
    .metric-yellow { border-color: rgba(245,158,11,.45); }
    .metric-purple { border-color: rgba(168,85,247,.45); }
    .metric-orange { border-color: rgba(249,115,22,.45); }

    .metric-label {
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .metric-value {
        font-size: clamp(19px, 1.45vw, 26px);
        font-weight: 800;
        color: white;
        margin-bottom: 14px;
        line-height: 1.15;
    }

    .metric-sub {
        font-size: 12px;
        color: #cbd5e1;
    }

    .cyan { color: #22d3ee; }
    .green { color: #4ade80; }
    .yellow { color: #fbbf24; }
    .purple { color: #e879f9; }
    .orange { color: #fb923c; }

    .chart-card {
        border: 1px solid rgba(255,255,255,.10);
        background: linear-gradient(145deg, rgba(18,27,37,.94), rgba(10,16,23,.94));
        border-radius: 10px;
        padding: 16px 16px 8px 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,.20);
        height: 100%;
        min-height: 370px;
    }

    .chart-title {
        font-size: 16px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 4px;
        text-transform: uppercase;
    }

    .section-title {
        margin-top: 18px;
        margin-bottom: 8px;
        color: #f8fafc;
        font-size: 18px;
        font-weight: 800;
        text-transform: uppercase;
    }

    .upload-card, .side-card {
        border: 1px solid rgba(255,255,255,.12);
        background: linear-gradient(145deg, rgba(18,27,37,.95), rgba(10,16,23,.95));
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }

    .side-title {
        font-size: 16px;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 8px;
        color: #f8fafc;
    }

    .small-muted {
        color: #cbd5e1;
        font-size: 12px;
        line-height: 1.5;
    }

    .stDataFrame {
        border: 1px solid rgba(255,255,255,.12);
        border-radius: 10px;
        overflow: hidden;
    }

    div[data-testid="stFileUploader"] section {
        background: rgba(255,255,255,.03);
        border: 1px dashed #e71d3c;
        border-radius: 8px;
    }

    div[data-testid="stFileUploader"] button {
        background: linear-gradient(90deg, #e71d3c, #b5122d);
        color: white;
        border: 0;
    }

    .stSelectbox div[data-baseweb="select"], .stTextInput input {
        background-color: #111923 !important;
        color: #f8fafc !important;
        border-color: rgba(255,255,255,.16) !important;
    }

    @media(max-width: 1500px) {
        .top-header {
            grid-template-columns: minmax(190px, 240px) minmax(280px, 1fr);
        }
        .header-card { min-height: 82px; }
    }

    @media(max-width: 1050px) {
        .top-header { grid-template-columns: 1fr; }
        .brand-box {
            border-right: none;
            border-bottom: 1px solid rgba(220,20,60,.45);
            padding-bottom: 12px;
            justify-content: center;
        }
        .title-box {
            border-right: none;
            min-width: unset;
            text-align: center;
        }
        .ac-grid { grid-template-columns: 1fr; }
        .ac-row { grid-template-columns: 150px 1fr; }
    }
</style>
""",
    unsafe_allow_html=True,
)

def br_num(valor, casas=2):
    try:
        return f"{float(valor):,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "0,00"

def limpar_numero_serie(valor):
    if pd.isna(valor):
        return 0.0
    s = str(valor).strip().replace('"', "")
    if s == "" or s.lower() == "nan":
        return 0.0
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except Exception:
        return 0.0

def limpar_texto(valor):
    if pd.isna(valor):
        return ""
    return str(valor).replace('""', '"').strip().strip('"')

def ler_csv_drawback_bytes(file_bytes):
    texto = file_bytes.decode("latin1", errors="ignore")
    linhas = [l.strip() for l in texto.splitlines() if l.strip()]
    if not linhas:
        return pd.DataFrame()

    cabecalho = linhas[0].replace(";;", "").strip().strip('"')
    colunas = [c.strip() for c in cabecalho.split("|")]

    registros = []
    for linha in linhas[1:]:
        linha = linha.replace(";;", "").strip().strip('"')
        partes = linha.split("|")
        if len(partes) < len(colunas):
            partes += [""] * (len(colunas) - len(partes))
        if len(partes) > len(colunas):
            partes = partes[: len(colunas)]
        registros.append(partes)

    df = pd.DataFrame(registros, columns=colunas)

    for col in df.columns:
        if "DESCRICAO" in col:
            df[col] = df[col].map(limpar_texto)

    for col in [
        "QUANTIDADE_AUTORIZADA",
        "NOVA_QUANTIDADE_AUTORIZADA",
        "QUANTIDADE_REALIZADA",
        "VALOR_AUTORIZADO",
        "NOVO_VALOR_AUTORIZADO",
        "VALOR_REALIZADO",
    ]:
        if col in df.columns:
            df[col] = df[col].map(limpar_numero_serie)

    if "QUANTIDADE_AUTORIZADA" in df.columns and "QUANTIDADE_REALIZADA" in df.columns:
        df["QTDE_SALDO_DBK"] = df["QUANTIDADE_AUTORIZADA"] - df["QUANTIDADE_REALIZADA"]

    if "VALOR_AUTORIZADO" in df.columns and "VALOR_REALIZADO" in df.columns:
        df["VALOR_SALDO_DBK"] = df["VALOR_AUTORIZADO"] - df["VALOR_REALIZADO"]

    if "VALOR_AUTORIZADO" in df.columns and "VALOR_REALIZADO" in df.columns:
        df["% CONSUMIDO (VALOR)"] = df.apply(
            lambda r: (r["VALOR_REALIZADO"] / r["VALOR_AUTORIZADO"] * 100)
            if r.get("VALOR_AUTORIZADO", 0) else 0,
            axis=1,
        )

    if "QUANTIDADE_AUTORIZADA" in df.columns and "QUANTIDADE_REALIZADA" in df.columns:
        df["% CONSUMIDO (QTD)"] = df.apply(
            lambda r: (r["QUANTIDADE_REALIZADA"] / r["QUANTIDADE_AUTORIZADA"] * 100)
            if r.get("QUANTIDADE_AUTORIZADA", 0) else 0,
            axis=1,
        )

    return df

def ler_arquivo_upload(uploaded_file):
    conteudo = uploaded_file.read()
    if uploaded_file.name.lower().endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(conteudo)) as z:
            csvs = [n for n in z.namelist() if n.lower().endswith(".csv")]
            if not csvs:
                raise ValueError("O ZIP não contém arquivo CSV.")
            with z.open(csvs[0]) as f:
                conteudo_csv = f.read()
        return ler_csv_drawback_bytes(conteudo_csv), conteudo, uploaded_file.name
    return ler_csv_drawback_bytes(conteudo), conteudo, uploaded_file.name

def carregar_ultimo_arquivo():
    if not ARQUIVO_ATUAL.exists():
        return pd.DataFrame(), None, None
    conteudo = ARQUIVO_ATUAL.read_bytes()
    nome = ARQUIVO_NOME.read_text("utf-8") if ARQUIVO_NOME.exists() else "arquivo_carregado.csv"
    data = ARQUIVO_DATA.read_text("utf-8") if ARQUIVO_DATA.exists() else ""
    if nome.lower().endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(conteudo)) as z:
            csvs = [n for n in z.namelist() if n.lower().endswith(".csv")]
            with z.open(csvs[0]) as f:
                conteudo_csv = f.read()
        return ler_csv_drawback_bytes(conteudo_csv), nome, data
    return ler_csv_drawback_bytes(conteudo), nome, data

def salvar_ultimo_arquivo(conteudo, nome):
    ARQUIVO_ATUAL.write_bytes(conteudo)
    ARQUIVO_NOME.write_text(nome, "utf-8")
    ARQUIVO_DATA.write_text(datetime.now().strftime("%d/%m/%Y %H:%M"), "utf-8")

def plot_bar(df, xcol, cor):
    base = df.copy()
    if base.empty or xcol not in base.columns or "DESCRICAO_COMPLEMENTAR_AUTORIZADA" not in base.columns:
        fig = go.Figure()
    else:
        base = base.sort_values(xcol, ascending=False).head(10).copy()
        base["DESCRICAO_GRAFICO"] = base["DESCRICAO_COMPLEMENTAR_AUTORIZADA"].astype(str).str[:34]
        fig = px.bar(
            base.sort_values(xcol),
            x=xcol,
            y="DESCRICAO_GRAFICO",
            orientation="h",
            text=xcol,
        )
        fig.update_traces(marker_color=cor, texttemplate="%{text:,.2f}", textposition="outside")
    fig.update_layout(
        height=310,
        margin=dict(l=8, r=22, t=8, b=28),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc", size=11),
        xaxis=dict(gridcolor="rgba(255,255,255,.12)", zerolinecolor="rgba(255,255,255,.16)"),
        yaxis=dict(gridcolor="rgba(255,255,255,.0)"),
    )
    return fig

def plot_consumo(realizado, autorizado, titulo_centro):
    consumido = (realizado / autorizado * 100) if autorizado else 0
    saldo = max(0, 100 - consumido)
    fig = go.Figure(
        data=[
            go.Pie(
                values=[consumido, saldo],
                labels=["Consumido", "Disponível"],
                hole=0.62,
                marker=dict(colors=["#e71d3c", "#35c6c9"]),
                textinfo="none",
            )
        ]
    )
    fig.add_annotation(
        text=f"<b>{br_num(consumido)}%</b><br>{titulo_centro}",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=18, color="#f8fafc"),
    )
    fig.update_layout(
        height=310,
        margin=dict(l=4, r=4, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc", size=11),
        legend=dict(orientation="v", y=0.5, x=0.76),
    )
    return fig

def preparar_tabela(df):
    colunas_preferidas = [
        "NCM",
        "NUMERO_ITEM_REPOSICAO",
        "DESCRICAO_COMPLEMENTAR_AUTORIZADA",
        "QUANTIDADE_AUTORIZADA",
        "QUANTIDADE_REALIZADA",
        "QTDE_SALDO_DBK",
        "VALOR_REALIZADO",
        "VALOR_AUTORIZADO",
        "VALOR_SALDO_DBK",
        "% CONSUMIDO (VALOR)",
        "% CONSUMIDO (QTD)",
    ]
    colunas = [c for c in colunas_preferidas if c in df.columns]
    return df[colunas].copy()

with st.sidebar:
    st.markdown(
        f"""
        <div class="upload-card" style="text-align:center;">
            <img src="data:image/png;base64,{LOGO_3S_BASE64}" style="max-width:210px;width:95%;margin-bottom:10px;">
            <div class="side-title">Reposição</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="upload-card"><div class="side-title">Upload de arquivo</div><div class="small-muted">Envie o arquivo CSV ou ZIP exportado do Drawback.</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Selecionar arquivo", type=["csv", "zip"], label_visibility="collapsed")
    st.markdown('<div class="small-muted">Formatos aceitos: CSV, ZIP</div></div>', unsafe_allow_html=True)

    if uploaded_file:
        try:
            df_upload, conteudo_upload, nome_upload = ler_arquivo_upload(uploaded_file)
            salvar_ultimo_arquivo(conteudo_upload, nome_upload)
            st.success("Arquivo carregado e salvo como versão atual.")
        except Exception as e:
            st.error(f"Erro ao ler arquivo: {e}")

    df, nome_arquivo, data_atualizacao = carregar_ultimo_arquivo()

    st.markdown('<div class="side-card"><div class="side-title">Arquivo atual</div>', unsafe_allow_html=True)
    if nome_arquivo:
        st.markdown(f'<div class="small-muted">✅ {nome_arquivo}<br>{data_atualizacao}<br>Registros: {len(df)}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="small-muted">Nenhum arquivo carregado.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="side-card"><div class="side-title">Filtros</div>', unsafe_allow_html=True)
    busca = st.text_input("Buscar", placeholder="NCM, item ou descrição")
    ncm_opcoes = ["Todos"]
    if not df.empty and "NCM" in df.columns:
        ncm_opcoes += sorted(df["NCM"].astype(str).unique().tolist())
    ncm_sel = st.selectbox("NCM", ncm_opcoes)
    if st.button("Limpar filtros", use_container_width=True):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

df_filtrado = df.copy()
if not df_filtrado.empty:
    if busca:
        mask = pd.Series(False, index=df_filtrado.index)
        for c in ["NCM", "NUMERO_ITEM_REPOSICAO", "DESCRICAO_COMPLEMENTAR_AUTORIZADA"]:
            if c in df_filtrado.columns:
                mask = mask | df_filtrado[c].astype(str).str.contains(busca, case=False, na=False)
        df_filtrado = df_filtrado[mask]
    if ncm_sel != "Todos" and "NCM" in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado["NCM"].astype(str) == str(ncm_sel)]

ultima = data_atualizacao or "Sem arquivo carregado"

st.markdown(
    f"""
<div class="top-header">
    <div class="brand-box">
        <img src="data:image/png;base64,{LOGO_3S_BASE64}">
    </div>
    <div class="title-box">
        <h1>REPOSIÇÃO</h1>
        <p>Controle de Saldos de Drawback</p>
    </div>
    <div class="header-card">
        <div class="header-label">Cliente</div>
        <div class="header-value">{DADOS_AC["razao_social"]}</div>
        <div class="header-sub">CNPJ: {DADOS_AC["beneficiario"]}</div>
    </div>
    <div class="header-card">
        <div class="header-label">Ato Concessório</div>
        <div class="header-value">{DADOS_AC["numero_ac"]}</div>
        <div class="header-sub">Situação: {DADOS_AC["situacao"]}</div>
    </div>
    <div class="header-card">
        <div class="header-label">Última atualização</div>
        <div class="header-value">{ultima}</div>
        <div class="header-sub">Dados do último arquivo carregado</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="ac-box">
    <div class="ac-title">Dados básicos do Ato Concessório</div>
    <div class="ac-grid">
        <div>
            <div class="ac-row"><div class="ac-key">Número do AC</div><div class="ac-val">{DADOS_AC["numero_ac"]}</div></div>
            <div class="ac-row"><div class="ac-key">Tipo</div><div class="ac-val">{DADOS_AC["tipo"]}</div></div>
            <div class="ac-row"><div class="ac-key">Situação do AC</div><div class="ac-val">{DADOS_AC["situacao"]}</div></div>
            <div class="ac-row"><div class="ac-key">Beneficiário</div><div class="ac-val">{DADOS_AC["beneficiario"]}</div></div>
            <div class="ac-row"><div class="ac-key">Razão Social</div><div class="ac-val">{DADOS_AC["razao_social"]}</div></div>
        </div>
        <div>
            <div class="ac-row"><div class="ac-key">Valor Total Importação (US$)</div><div class="ac-val">{DADOS_AC["valor_total_importacao"]}</div></div>
            <div class="ac-row"><div class="ac-key">Valor Total MI (US$)</div><div class="ac-val">{DADOS_AC["valor_total_mi"]}</div></div>
            <div class="ac-row"><div class="ac-key">Valor Total Exportação FOB (US$)</div><div class="ac-val">{DADOS_AC["valor_total_exportacao_fob"]}</div></div>
            <div class="ac-row"><div class="ac-key">Valor Total Reposição (US$)</div><div class="ac-val">{DADOS_AC["valor_total_reposicao"]}</div></div>
            <div class="ac-row"><div class="ac-key">Vigência</div><div class="ac-val">{DADOS_AC["vigencia"]}</div></div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

if df_filtrado.empty:
    st.info("Envie um CSV ou ZIP do Drawback no menu lateral para carregar o dashboard.")
    st.stop()

total_valor_aut = df_filtrado.get("VALOR_AUTORIZADO", pd.Series(dtype=float)).sum()
total_valor_real = df_filtrado.get("VALOR_REALIZADO", pd.Series(dtype=float)).sum()
total_valor_saldo = df_filtrado.get("VALOR_SALDO_DBK", pd.Series(dtype=float)).sum()
total_qtd_aut = df_filtrado.get("QUANTIDADE_AUTORIZADA", pd.Series(dtype=float)).sum()
total_qtd_real = df_filtrado.get("QUANTIDADE_REALIZADA", pd.Series(dtype=float)).sum()
total_qtd_saldo = df_filtrado.get("QTDE_SALDO_DBK", pd.Series(dtype=float)).sum()
itens_com_saldo = int((df_filtrado.get("VALOR_SALDO_DBK", pd.Series(dtype=float)) > 0).sum())

m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.markdown(f'<div class="metric-card metric-cyan"><div class="metric-label cyan">Saldo total (USD)</div><div class="metric-value">{br_num(total_valor_saldo)}</div><div class="metric-sub">Valores em USD</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card metric-green"><div class="metric-label green">Saldo total (Qtd.)</div><div class="metric-value">{br_num(total_qtd_saldo)}</div><div class="metric-sub">Quantidade disponível</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-card metric-yellow"><div class="metric-label yellow">Itens com saldo</div><div class="metric-value">{itens_com_saldo}</div><div class="metric-sub">Materiais disponíveis</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-card metric-purple"><div class="metric-label purple">Valor utilizado (USD)</div><div class="metric-value">{br_num(total_valor_real)}</div><div class="metric-sub">Total já utilizado</div></div>', unsafe_allow_html=True)
with m5:
    st.markdown(f'<div class="metric-card metric-orange"><div class="metric-label orange">Qtd. utilizada</div><div class="metric-value">{br_num(total_qtd_real)}</div><div class="metric-sub">Quantidade já utilizada</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
g1, g2 = st.columns(2)
with g1:
    st.markdown('<div class="chart-card"><div class="chart-title">Saldo por valor (USD)</div>', unsafe_allow_html=True)
    st.plotly_chart(plot_bar(df_filtrado, "VALOR_SALDO_DBK", "#e71d3c"), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
with g2:
    st.markdown('<div class="chart-card"><div class="chart-title">Saldo por quantidade</div>', unsafe_allow_html=True)
    st.plotly_chart(plot_bar(df_filtrado, "QTDE_SALDO_DBK", "#35c6c9"), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

g3, g4 = st.columns(2)
with g3:
    st.markdown('<div class="chart-card"><div class="chart-title">Percentual consumido por valor</div>', unsafe_allow_html=True)
    st.plotly_chart(plot_consumo(total_valor_real, total_valor_aut, "VALOR"), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
with g4:
    st.markdown('<div class="chart-card"><div class="chart-title">Percentual consumido por quantidade</div>', unsafe_allow_html=True)
    st.plotly_chart(plot_consumo(total_qtd_real, total_qtd_aut, "QTD."), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-title">Saldo detalhado</div>', unsafe_allow_html=True)

tabela = preparar_tabela(df_filtrado)
column_config = {}

for pcol in ["% CONSUMIDO (VALOR)", "% CONSUMIDO (QTD)"]:
    if pcol in tabela.columns:
        column_config[pcol] = st.column_config.ProgressColumn(
            pcol,
            format="%.2f%%",
            min_value=0,
            max_value=100,
        )

for col in [
    "QUANTIDADE_AUTORIZADA",
    "QUANTIDADE_REALIZADA",
    "QTDE_SALDO_DBK",
    "VALOR_REALIZADO",
    "VALOR_AUTORIZADO",
    "VALOR_SALDO_DBK",
]:
    if col in tabela.columns:
        column_config[col] = st.column_config.NumberColumn(col, format="%.2f")

st.dataframe(
    tabela,
    use_container_width=True,
    hide_index=True,
    height=640,
    column_config=column_config,
)

st.caption("* Percentuais consumidos calculados com base nos valores/quantidades realizados versus autorizados.")
st.caption("Observação: no Streamlit Cloud, o arquivo enviado fica salvo enquanto o aplicativo permanecer ativo. Para persistência definitiva, recomenda-se usar armazenamento externo.")

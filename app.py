import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Vendas Premium",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Personalizado ---
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 800;
        text-shadow: 0px 4px 15px rgba(0, 198, 255, 0.3);
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 198, 255, 0.2);
        border-color: rgba(0, 198, 255, 0.3);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
    }
    .stMetric label {
        color: #a0a0b8 !important;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stMetric div {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: 700;
        text-shadow: 0 2px 10px rgba(255, 255, 255, 0.1);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stSelectbox, .stMultiselect, .stSlider, .stDateInput {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #a0a0b8;
        border-radius: 8px;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%) !important;
        color: white !important;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0, 198, 255, 0.3);
    }
    .info-box {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 20px;
        border-left: 3px solid #00c6ff;
        margin-top: 15px;
    }
    .progress-bar {
        height: 6px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 3px;
        overflow: hidden;
        margin: 10px 0;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        border-radius: 3px;
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin-top: 10px;
    }
    .stat-item {
        background: rgba(255, 255, 255, 0.02);
        padding: 10px;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- Carregar e Tratar Dados ---
@st.cache_data
def load_and_prepare_data(filepath="vendas_tratadas.csv"):
    try:
        df = pd.read_csv(filepath)
        df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, errors="coerce")
        df.dropna(subset=['Order Date'], inplace=True)
        df['Month_Year'] = df['Order Date'].dt.to_period('M').astype(str)
        df['Year'] = df['Order Date'].dt.year
        df['Quarter'] = df['Order Date'].dt.quarter
        df['Day_of_Week'] = df['Order Date'].dt.day_name()
        df['Hour'] = df['Order Date'].dt.hour
        return df
    except FileNotFoundError:
        st.error(f"Erro: O arquivo '{filepath}' não foi encontrado. Por favor, verifique o caminho.")
        st.stop()
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar os dados: {e}")
        st.stop()

df = load_and_prepare_data()

# --- Funções de Lógica ---
def calculate_kpis(df):
    receita_total = df['Sales'].sum()
    num_pedidos = df['Order ID'].nunique()
    clientes_unicos = df['Customer Name'].nunique()
    ticket_medio = receita_total / clientes_unicos if clientes_unicos > 0 else 0
    return receita_total, num_pedidos, clientes_unicos, ticket_medio

def get_trend_growth(df):
    receita_mensal = df.groupby('Month_Year')['Sales'].sum()
    if len(receita_mensal) > 1:
        crescimento = (receita_mensal.iloc[-1] - receita_mensal.iloc[-2]) / receita_mensal.iloc[-2] * 100
    else:
        crescimento = 0
    return crescimento

def get_plotly_template():
    return {
        'layout': {
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'font': {'color': 'white'},
            'xaxis': {'gridcolor': 'rgba(255,255,255,0.1)'},
            'yaxis': {'gridcolor': 'rgba(255,255,255,0.1)'}
        }
    }

# --- Sidebar de Filtros ---
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); 
                border-radius: 15px; margin-bottom: 25px; box-shadow: 0 8px 25px rgba(0, 198, 255, 0.3);'>
        <h2 style='color: white; margin: 0; font-weight: 700;'>🚀 Filtros Avançados</h2>
    </div>
    """, unsafe_allow_html=True)
    
    anos = sorted(df['Year'].unique(), reverse=True)
    trimestres = sorted(df['Quarter'].unique())
    regioes = sorted(df['Region'].unique())
    dias_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    ano_selecionado = st.selectbox("**📅 Ano:**", ["Todos"] + list(anos))
    trimestre_selecionado = st.selectbox("**📊 Trimestre:**", ["Todos"] + list(trimestres))
    regioes_selecionadas = st.multiselect("**🌎 Região:**", regioes, default=regioes)
    dias_selecionados = st.multiselect("**📅 Dias da Semana:**", dias_semana, default=dias_semana)
    min_valor, max_valor = st.slider(
        "**💰 Faixa de Valores (R$):**",
        min_value=float(df['Sales'].min()),
        max_value=float(df['Sales'].max()),
        value=(float(df['Sales'].min()), float(df['Sales'].max()))
    )

# --- Aplicação de Filtros ---
df_filtrado = df.copy()
if ano_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Year'] == ano_selecionado]
if trimestre_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Quarter'] == trimestre_selecionado]
df_filtrado = df_filtrado[
    (df_filtrado['Region'].isin(regioes_selecionadas)) &
    (df_filtrado['Day_of_Week'].isin(dias_selecionados)) &
    (df_filtrado['Sales'] >= min_valor) &
    (df_filtrado['Sales'] <= max_valor)
]

# --- Layout Principal ---
col_logo, col_title, _ = st.columns([1, 3, 1])
with col_logo:
    st.markdown("<div style='text-align: center; font-size: 3rem; margin-top: 10px;'>🚀</div>", unsafe_allow_html=True)
with col_title:
    st.markdown('<h1 class="main-header">Dashboard de Vendas Premium</h1>', unsafe_allow_html=True)

# --- Indicadores Principais (KPIs) ---
st.markdown("### 📊 Indicadores Principais")
receita_total, num_pedidos, clientes_unicos, ticket_medio = calculate_kpis(df_filtrado)
crescimento_receita = get_trend_growth(df_filtrado)

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Receita Total", f"R$ {receita_total:,.2f}", f"{crescimento_receita:+.1f}%" if len(df_filtrado) > 1 else None)
col2.metric("🧾 Total de Pedidos", f"{num_pedidos:,}")
col3.metric("🎟️ Ticket Médio", f"R$ {ticket_medio:,.2f}")
col4.metric("👥 Clientes Únicos", f"{clientes_unicos:,}")

# --- Gráficos Avançados (Tabs) ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📈 Tendência", "🏆 Produtos", "🌎 Regiões", "👥 Clientes", "⏰ Temporal", "📊 Insights"])
plotly_template = get_plotly_template()

with tab1:
    st.subheader("📈 Evolução Mensal da Receita")
    receita_mensal_df = df_filtrado.groupby('Month_Year')['Sales'].sum().reset_index()
    fig = px.line(receita_mensal_df, x='Month_Year', y='Sales', labels={'Sales': 'Receita (R$)', 'Month_Year': 'Mês/Ano'})
    fig.update_traces(line=dict(color='#00c6ff', width=4), mode='lines+markers', marker=dict(size=8, color='#0072ff'))
    fig.update_layout(**plotly_template['layout'])
    st.plotly_chart(fig, use_container_width=True)
    
    col1_tab1, col2_tab1 = st.columns(2)
    with col1_tab1:
        st.subheader("📊 Análise de Tendência")
        st.metric("📈 Variação Mensal", f"{crescimento_receita:+.1f}%")
        tendencia = "↗️ Alta" if crescimento_receita > 0 else "↘️ Baixa" if crescimento_receita < 0 else "➡️ Estável"
        st.info(f"**Tendência:** {tendencia}")
    with col2_tab1:
        st.subheader("🎯 Performance Mensal")
        if len(receita_mensal_df) > 0 and receita_mensal_df['Sales'].max() > 0:
            progresso = min(100, (receita_mensal_df['Sales'].iloc[-1] / receita_mensal_df['Sales'].max()) * 100)
            st.markdown(f'<div class="progress-bar"><div class="progress-fill" style="width: {progresso}%;"></div></div>', unsafe_allow_html=True)
            st.caption(f"{progresso:.1f}% do melhor mês")

with tab2:
    st.subheader("🏆 Análise de Produtos")
    col1, col2 = st.columns(2)
    with col1:
        produtos_receita = df_filtrado.groupby('Product Name')['Sales'].sum().nlargest(10).reset_index()
        fig = px.bar(produtos_receita, x='Sales', y='Product Name', orientation='h', title="Top 10 Produtos por Receita")
        fig.update_traces(marker_color='#00c6ff')
        fig.update_layout(**plotly_template['layout'])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        qtd_produtos = df_filtrado['Product Name'].value_counts().nlargest(10)
        fig = px.bar(x=qtd_produtos.values, y=qtd_produtos.index, orientation='h', title="Top 10 Produtos por Quantidade")
        fig.update_traces(marker_color='#0072ff')
        fig.update_layout(**plotly_template['layout'])
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("🌎 Análise Geográfica")
    col1, col2 = st.columns(2)
    with col1:
        regioes_df = df_filtrado.groupby('Region')['Sales'].sum().reset_index()
        fig = px.pie(regioes_df, values='Sales', names='Region', title="Distribuição por Região")
        fig.update_layout(**plotly_template['layout'])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.treemap(regioes_df, path=['Region'], values='Sales', title="Mapa de Árvore por Região", color='Sales', color_continuous_scale='Blues')
        fig.update_layout(**plotly_template['layout'])
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("👥 Análise de Clientes")
    col1, col2 = st.columns(2)
    with col1:
        ticket_clientes = df_filtrado.groupby('Customer Name')['Sales'].mean().nlargest(10).reset_index()
        fig = px.bar(ticket_clientes, x='Sales', y='Customer Name', orientation='h', title="Top 10 Clientes por Ticket Médio")
        fig.update_traces(marker_color='#00c6ff')
        fig.update_layout(**plotly_template['layout'])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        freq_compras = df_filtrado['Customer Name'].value_counts().nlargest(10)
        fig = px.bar(x=freq_compras.values, y=freq_compras.index, orientation='h', title="Top 10 Clientes por Frequência")
        fig.update_traces(marker_color='#0072ff')
        fig.update_layout(**plotly_template['layout'])
        st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.subheader("⏰ Análise Temporal")
    col1, col2 = st.columns(2)
    with col1:
        vendas_hora = df_filtrado.groupby('Hour')['Sales'].sum()
        fig = px.bar(x=vendas_hora.index, y=vendas_hora.values, title="Vendas por Hora do Dia", labels={'x': 'Hora', 'y': 'Vendas (R$)'})
        fig.update_traces(marker_color='#00c6ff')
        fig.update_layout(**plotly_template['layout'])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        vendas_dia = df_filtrado.groupby('Day_of_Week')['Sales'].sum().reindex(dias_ordem, fill_value=0)
        fig = px.bar(x=vendas_dia.index, y=vendas_dia.values, title="Vendas por Dia da Semana", labels={'x': 'Dia da Semana', 'y': 'Vendas (R$)'})
        fig.update_traces(marker_color='#0072ff')
        fig.update_layout(**plotly_template['layout'])
        st.plotly_chart(fig, use_container_width=True)

with tab6:
    st.subheader("📊 Insights e Estatísticas")
    if not df_filtrado.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("📦 Produtos Únicos", df_filtrado['Product Name'].nunique())
        col2.metric("🏢 Regiões Ativas", df_filtrado['Region'].nunique())
        col3.metric("📅 Período (dias)", (df_filtrado['Order Date'].max() - df_filtrado['Order Date'].min()).days)

        col4, col5 = st.columns(2)
        with col4:
            st.info(f"""
            **📈 Estatísticas de Vendas:**
            - Venda Média: R$ {df_filtrado['Sales'].mean():.2f}
            - Maior Venda: R$ {df_filtrado['Sales'].max():.2f}
            - Menor Venda: R$ {df_filtrado['Sales'].min():.2f}
            """)
        with col5:
            dias_totais = (df_filtrado['Order Date'].max() - df_filtrado['Order Date'].min()).days
            pedidos_por_dia = round(num_pedidos / max(1, dias_totais), 1)
            st.success(f"""
            **🎯 Insights:**
            - {pedidos_por_dia} pedidos por dia em média
            - Ticket médio: R$ {ticket_medio:.2f}
            - {df_filtrado['Product Name'].nunique()} produtos únicos vendidos
            """)
    else:
        st.warning("Nenhum dado encontrado com os filtros selecionados.")
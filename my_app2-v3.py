import pandas as pd
import yfinance as yf
import streamlit as st
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def extract_data(ticker, start, end):
    data = yf.download(ticker, start, end)
    data = data.reset_index()
    return data


today = dt.date.today().strftime('%Y-%m-%d')
tickers = ['ITUB3.SA', 'BBDC3.SA', 'BBAS3.SA', 'BRSR6.SA']
ticker = st.sidebar.selectbox(
    'Escolha a Ação de um dos Bancos Listados na B3',
     tickers)

line_colors = ["#EC7000", "#269428", "#F8D117", "#2a36b8"]
color = line_colors[tickers.index(ticker)]

time_of_analizes = st.sidebar.radio(
        "Escolha o período de análise",
        ('1 ano', '2 anos', '3 anos', '4 anos', '5 anos')
    ) 

if (time_of_analizes == '1 ano'):
    anos = 1
elif (time_of_analizes == '2 anos'):
    anos = 2
elif (time_of_analizes == '3 anos'):
    anos = 3
elif (time_of_analizes == '4 anos'):
    anos = 4
else:
    anos = 5

start = dt.datetime.today()-dt.timedelta(anos * 365)

df = extract_data(ticker, start=start, end=today)
#data2 = extract_data(tickers[1], start=start, end=today)
#data3 = extract_data(tickers[2], start=start, end=today)
#data4 = extract_data(tickers[3], start=start, end=today)
#data5 = extract_data(tickers[4], start=start, end=today)  

st.title(f"Preço de Fechamento na B3 no(s) Último(s) {anos} ano(s)")
fig = make_subplots(specs=[[{"secondary_y": True}]], y_title='R$')

fig.add_trace(go.Scatter(
    x=df['Date'], y=df['Close'], name=ticker, line=dict(color=color)))

fig.layout.update(xaxis_rangeslider_visible=True)
                  
fig.update_layout(
    xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(0, 0, 0)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Roboto',
                size=12,
                color='rgb(82,82,82)'),
        ),
    yaxis=dict(
            showline=True,
            showgrid=False,
            zeroline=True,
            showticklabels=True,
            ticks='outside',
            linecolor='rgb(82, 82, 82)',
            linewidth=3,
            tickfont=dict(
                family='Roboto',
                size=12,
                color='rgb(0,0,0)')
        ),
    plot_bgcolor='rgb(255,255,255)',     
)
st.plotly_chart(fig, use_container_width=True)

st.title('Indicadores Técnicos no Período')
max_periodo = max(df['Close'])
data_max = df['Date'][df.set_index('Close').index.get_loc(max_periodo)].strftime('%Y-%m-%d')
min_periodo = min(df['Close'])
data_min = df['Date'][df.set_index('Close').index.get_loc(min_periodo)].strftime('%Y-%m-%d')
valor_inicial = df['Close'][0]
valor_final = df['Close'].tail(1).values

variacao_periodo = ((valor_final[0] / valor_inicial) - 1) * 100 
if variacao_periodo > 0:
  sinal = "+"
else:
  sinal = "-"

col1, col2, col3 = st.columns(3)
col1.metric("Valor Máximo", f"R$ {round(max_periodo, 2)}", f"{data_max}")
col2.metric("Valor Mínimo", f"R$ {round(min_periodo, 2)}", f"-{data_min}")
col3.metric("Variação", f"{round(variacao_periodo, 2)}%", sinal)



st.title('Desempenho dos Bancos Durante Governo Escolhido')
presidente = ticker = st.sidebar.selectbox(
    'Escolha o(a) Presidente(a)',
     ['FHC', 'Lula', 'Dilma', 'Temer', 'Bolsonaro'])

start = '1994-01-01'
today = dt.date.today().strftime('%Y-%m-%d')

#tickers = ['ITUB3.SA', 'BBDC3.SA', 'BBAS3.SA', 'BRSR6.SA']
dfb = yf.download(tickers, start, today)
bancos = dfb['Close'][tickers]

fhc = ['1995-01-01', '2002-12-31']
lula = ['2003-01-01', '2010-12-31']
dilma = ['2011-01-01', '2016-08-31']
temer = ['2016-09-01', '2018-12-31']
bolsonaro = ['2019-01-01', dt.date.today().strftime('%Y-%m-%d')]

periodo = {
    'FHC': {'start': fhc[0], 'end': fhc[1]},
    'Lula': {'start': lula[0], 'end': lula[1]},
    'Dilma': {'start': dilma[0], 'end': dilma[1]},
    'Temer': {'start': temer[0], 'end': temer[1]},
    'Bolsonaro': {'start': bolsonaro[0], 'end': bolsonaro[1]},
}

dfg = bancos.iloc[(bancos.index >= periodo[presidente]['start']) & (bancos.index <= periodo[presidente]['end'])]


fig = make_subplots(specs=[[{"secondary_y": True}]], y_title='R$')


fig.add_trace(go.Scatter(
    x=dfg.index,
    y=dfg[tickers[0]],
    name=tickers[0],
    line=dict(color="#EC7000")
             ))
fig.add_trace(go.Scatter(
    x=dfg.index,
    y=dfg[tickers[1]],
    name=tickers[1],
    line=dict(color="#269428")
             ))
fig.add_trace(go.Scatter(
    x=dfg.index,
    y=dfg[tickers[2]],
    name=tickers[2],
    line=dict(color="#F8D117")
             ))
fig.add_trace(go.Scatter(
    x=dfg.index,
    y=dfg[tickers[3]],
    name=tickers[3],
    #line=dict(color="#2a36b8")
             ))
#fig
st.plotly_chart(fig, use_container_width=True)


st.title('Comparativo entre bancos privados internacionais e nacionais')

tickers1 = ['DB', 'ITUB4.SA', 'BBDC4.SA', 'BAC', 'WFC']
start = '1995-01-01'
end = dt.date.today().strftime('%Y-%m-%d')

df1 = yf.download(tickers1, start, today)
df1.head()

bancos1 = df1['Close'][tickers1]

fig = make_subplots(specs=[[{"secondary_y": True}]])


fig.add_trace(go.Scatter(
    x=bancos1.index,
    y=bancos1[tickers1[0]],
    name=tickers1[0],
    line=dict(color="#EC7000")
             ))
fig.add_trace(go.Scatter(
    x=bancos1.index,
    y=bancos1[tickers1[1]],
    name=tickers1[1],
    line=dict(color="#269428")
             ))
fig.add_trace(go.Scatter(
    x=bancos1.index,
    y=bancos1[tickers1[2]],
    name=tickers1[2],
    line=dict(color="#F8D117")
             ))
fig.add_trace(go.Scatter(
    x=bancos1.index,
    y=bancos1[tickers1[3]],
    name=tickers1[3],
    line=dict(color="#2a36b8")
             ))
fig.add_trace(go.Scatter(
    x=bancos1.index,
    y=bancos1[tickers1[4]],
    name=tickers1[4]
             ))


st.plotly_chart(fig, use_container_width=True)
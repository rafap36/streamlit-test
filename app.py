import streamlit as st
import altair as alt
import pandas as pd
from PIL import Image


#CONFIGURAÇÕES DE PÁGINA
st.set_page_config(
  page_title = 'DASHBOARD DE VENDAS',
  page_icon = ':page_facing_up:',
  layout = 'wide',
  initial_sidebar_state = 'expanded',
  menu_items = {
    'About': 'Rec36 property'
  }
)


# criar o dataframe
df = pd.read_excel(
  io = './Datasets/system_extraction.xlsx',
  engine = 'openpyxl',
  sheet_name = 'salesreport',
  usecols = 'A:J',
  nrows = 4400
)

# criar o sidebar

with st.sidebar:
  logo_teste = Image.open('./Mídia/logo vizion.png')
  st.image(logo_teste, width=300)
  st.subheader('MENU - DASHBOARD DE VENDAS')

  fVendedor = st.selectbox(
    'Selecione o vendedor:',
    options=df['Vendedor'].unique()
    )

  produtofiltro = df['Produto vendido'].unique()
  produtofiltro = sorted(produtofiltro, reverse=False)
  fProduto = st.selectbox(
    'Selecione o produto:',
    options=produtofiltro
  )

  fCliente = st.selectbox(
    'Selecione o cliente:',
    options=df['Cliente'].unique()
  )


#tabela quantidade vendida por produto

tabl_qtde_produto = df.loc[
  (df['Vendedor'] == fVendedor)
  &
  (df['Cliente'] == fCliente)
  ]

tabl_qtde_produto = tabl_qtde_produto.groupby(['Produto vendido'])[['Quantidade', 'Preço', 'Valor Pedido']].sum().reset_index()
#Correção do erro:TypeError: datetime64 type does not support sum operations (específicar os campos a serem somados.)
#df.groupby(['City'])[['Quantity Ordered', 'Price Each', 'Total Price']].sum()



#tabela de vendas e margens

tab_vendas_margem = df.loc[
  (df['Vendedor'] == fVendedor)
  &
  (df['Cliente'] == fCliente)
  &
  (df['Produto vendido'] == fProduto)
]

#tabela de vendas por vendedor

tab_vendas_vendedor = df.loc[
  (df['Cliente'] == fCliente)
  &
  (df['Produto vendido'] == fProduto)
]

tab_vendas_vendedor = tab_vendas_vendedor.groupby(['Vendedor'])[['Quantidade', 'Valor Pedido', 'Margem Lucro']].sum().reset_index()



#Vendas por cliente

tab_vendas_cliente = df.loc[
  (df['Vendedor'] == fVendedor)
  &
  (df['Produto vendido'] == fProduto)
]

tab_vendas_cliente = tab_vendas_cliente.groupby(['Cliente'])[['Quantidade', 'Valor Pedido', 'Margem Lucro']].sum().reset_index()



#vendas mensais

tab_vendas_mensais = df.loc[
  (df['Vendedor'] == fVendedor)
  &
  (df['Cliente'] == fCliente)
  &
  (df['Produto vendido'] == fProduto)
]

tab_vendas_mensais['mm'] = tab_vendas_mensais['Data'].dt.strftime('%m/%Y')


######## PADÂO DE COR DOS GRÁFICOS ###########

cor_grafico = '#FF7F00'

#GRÁFICO 1.0 Quantidade vendida por produto
graf1_0_qtd_produto = alt.Chart(tabl_qtde_produto).mark_bar(
  color = cor_grafico,
  cornerRadiusTopLeft = 9,
  cornerRadiusTopRight= 9,
).encode(
  x = 'Produto vendido',
  y = 'Quantidade',
  tooltip = ['Produto vendido', 'Quantidade']
).properties(
  title = 'QUANTIDADE VENDIDA POR PRODUTOS'
).configure_axis(
  grid = False
).configure_view(
  strokeWidth = 0
)



#GRÁFICO 1.1 Valor da venda por produto
graf1_1_valor_produto = alt.Chart(tabl_qtde_produto).mark_bar(
  color = cor_grafico,
  cornerRadiusTopLeft = 9,
  cornerRadiusTopRight= 9,
).encode(
  x = 'Produto vendido',
  y = 'Quantidade',
  tooltip = ['Produto vendido', 'Valor Pedido']
).properties(
  title = 'VALOR TOTAL POR PRODUTOS'
).configure_axis(
  grid = False
).configure_view(
  strokeWidth = 0
)



#GRÁFICO vendas por vendedor
graf2_vendas_vendedor = alt.Chart(tab_vendas_vendedor).mark_arc(
  innerRadius=100,
  outerRadius=150
).encode(
  theta=alt.Theta(field='Valor Pedido', type='quantitative', stack=True),
  color=alt.Color(
    field='Vendedor',
    type='nominal'
  ),
  tooltip=['Vendedor', 'Valor Pedido']
).properties(
  title='VALOR DE VENDA POR VENDEDOR',
  height=500,
  width=560
)
rot2Ve = graf2_vendas_vendedor.mark_text(radius=210,size=14).encode(text='Vendedor')
rot2Vp = graf2_vendas_vendedor.mark_text(radius=180, size=12).encode(text='Valor Pedido')


#GRÁFICO de vendas por cliente
graf3_vendas_cliente = alt.Chart(tab_vendas_cliente).mark_bar(
  color = cor_grafico,
  cornerRadiusTopLeft = 9,
  cornerRadiusTopRight= 9,
).encode(
  x = 'Cliente',
  y = 'Valor Pedido',
  tooltip = ['Cliente', 'Valor Pedido']
).properties(
  title = 'VENDAS POR CLIENTE'
).configure_axis(
  grid = False
).configure_view(
  strokeWidth = 0
)



#GRÁFICO Vendas mensais
graf5_vendas_mensais = alt.Chart(tab_vendas_mensais).mark_line(
  color = cor_grafico
).encode(
  alt.X('monthdate(Data):T'),
  y = 'Valor Pedido:Q',
).properties(
  title = 'VENDAS MENSAIS'
).configure_axis(
  grid = False
).configure_view(
  strokeWidth = 0
)


######  PÁGINA PRINCIPAL ########
total_vendas = round(tab_vendas_margem['Valor Pedido'].sum(), 2)
total_margem = round(tab_vendas_margem['Margem Lucro'].sum(), 2)
porc_margem = int(100*total_margem/total_vendas)

st.header(":page_facing_up: DASHBOARD DE VENDAS")

dst1, dst2, dst3, dst4 = st.columns([1,1,1,2.5])

with dst1:
  st.write('**VENDAS TOTAIS:**')
  st.info(f'R$ {total_vendas}')

with dst2:
  st.write('**MARGEM TOTAL:**')
  st.info(f'R$ {total_margem}')

with dst3:
  st.write('**MARGEM %:**')
  st.info(f'{porc_margem}%')

st.markdown('---')

#COLUNA DOS GRÁFICOS

col1, col2, col3 = st.columns([1,1,1])

with col1:
  st.altair_chart(graf3_vendas_cliente, use_container_width=True)
  st.altair_chart(graf5_vendas_mensais, use_container_width=True)

with col2:
  st.altair_chart(graf1_0_qtd_produto, use_container_width=True)
  st.altair_chart(graf1_1_valor_produto, use_container_width=True)

with col3:
  st.altair_chart(graf2_vendas_vendedor + rot2Ve + rot2Vp)


st.markdown('---')

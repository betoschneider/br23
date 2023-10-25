# ### Campeonato Brasileiro 2023
# ##### Projeção da classificação final do Campeonato Brasileiro 2023
# **Mémória de cálculo da projeção**<br>
# *mpm x prm + mpv x prv*<br>
# 
# ###### **mpm**: média de pontos como mandante;<br>**mpv**: média de pontos como visitante;<br>**prm**: partidas restantes como mandante;<br>**prv**: partidas restantes como visitante.
# 

#importação das biblioteca
import pandas as pd
from etl import ETL
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

pd.options.mode.chained_assignment = None

arquivo = 'https://raw.githubusercontent.com/betoschneider/br23/main/tabela_br23.csv'
base = ETL(arquivo)
tabela_consolidada = base.get_tabela()
max_rodada = int(tabela_consolidada['jogos_total'].max())

#projecao na rodada mais recente
ultima_projecao = tabela_consolidada[tabela_consolidada['rodada_projecao'] == max_rodada]
ultima_projecao = ultima_projecao[['classificacao', 'time', 'pontos_finais']]


#visualização

######################################
#                                    #
# criando um dashboard com streamlit #
#                                    #
######################################

#configurando o layout de página
st.set_page_config(layout='wide')

#título
st.header('Brasileirão 2023: Projeção de pontos na última rodada')
st.markdown('###### Um exemplo de dashboard em Python com Streamlit  :sunglasses:')


#filtros
time = st.sidebar.selectbox('Time', tabela_consolidada['time'].unique())
tabela_consolidada_filtro = tabela_consolidada[(tabela_consolidada['time']==time) & (tabela_consolidada['rodada_projecao']==max_rodada)]

#colunas na página
col1, col2 = st.columns(2)
col3, col0 = st.columns(2)
col4, col5, col6 = st.columns(3)

#cores das linhas e barras
cores = px.colors.qualitative.Pastel + px.colors.qualitative.Pastel1

#grafico 1: projecao atual
fig1 = px.bar(tabela_consolidada[tabela_consolidada['rodada_projecao'] == max_rodada], x='pontos_finais', y='time', color='time', 
              title='Projeção atual', orientation='h', 
              text='pontos_finais',
              color_discrete_sequence=cores,
              labels={'pontos_finais':'Pontos projetados', 'time': 'Time'}
              )
fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) #rótulo de dados da barra
fig1.update_yaxes(tickfont_size=11) #tamanho da fonte do rótulo do eixo y
fig1.update_layout(showlegend=False)

#tabela_consolidada[df_consolidado['rodada_projecao'] == max_rodada]
col1.plotly_chart(fig1, use_container_width=True)

#grafico 2: historico projecao
fig2 = px.line(tabela_consolidada, x='rodada_projecao', y='pontos_finais', color='time',
               title='Histórico das projeções', 
               color_discrete_sequence=cores,
               labels={'pontos_finais':'Pontos projetados', 'rodada_projecao': 'Rodada'}
               )
fig2.update_layout(showlegend=False)
col2.plotly_chart(fig2, use_container_width=True)


#resultado por time
#st.header(str(time), divider='grey')
col3.header(str(time))
col4.markdown(
    '''###### Realizado até a %sª rodada 
    %sº lugar
    %sv %se %sd
    %s pontos (%s%% de aproveitamento)
    %s gols marcados
    %s gols de saldo
     ''' % (max_rodada, str(int(tabela_consolidada_filtro['classificacao'].max())),
             str(int(tabela_consolidada_filtro['vitoria_total'].max())),
             str(int(tabela_consolidada_filtro['empate_total'].max())),
             str(int(tabela_consolidada_filtro['derrota_total'].max())),
             str(int(tabela_consolidada_filtro['pontos_total'].max())),
             str(round(tabela_consolidada_filtro['aproveitamento_total'].max() * 100, 2)),
             str(int(tabela_consolidada_filtro['gols_marcados_total'].max())),
             str(int(tabela_consolidada_filtro['saldo_gols_total'].max()))
             )
)

col5.markdown(
        '''###### Projeção na rodada atual
        %s pontos projetados ao final do campeonato
        ''' % (int(tabela_consolidada_filtro['pontos_finais'].max()))
)

st.link_button('Meu perfil no LinkedIn', 'https://www.linkedin.com/in/robertoschneider/')

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

#base boca de jacare
tabela_jacare = base.get_tabela_jacare()
tabela_jacare.rename(columns={'pontos_projecao': 'pontos', 'rodada_projecao': 'rodada'}, inplace=True)


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

#barra lateral
#filtros
time = st.sidebar.selectbox('Time', tabela_consolidada['time'].unique())
tabela_consolidada_filtro = tabela_consolidada[(tabela_consolidada['time']==time) & (tabela_consolidada['rodada_projecao']==max_rodada)]

#resultado do filtro
#resultado por time
st.sidebar.header('', divider='grey')
st.sidebar.header(str(time))
st.sidebar.markdown(
    '''###### Realizado até a %sª rodada 
    %sº lugar
    %sv %se %sd
    %s pontos 
    %s%% de aproveitamento
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
st.sidebar.markdown(
        '''###### Projeção na rodada atual
        %s pontos projetados
        ''' % (int(tabela_consolidada_filtro['pontos_finais'].max()))
)
st.sidebar.header('', divider='grey')

#principal
#colunas na página
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)


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

#grafico 3: boca de jacare
fig3 = px.line(tabela_jacare, x='rodada', y='pontos', color='classificacao',
               color_discrete_sequence=cores,
               labels={'rodada':'Rodada', 'pontos': 'Pontos'},
               title='Líder x Pontuação máxima do 2º colocado'
               )
#rótulo de dados na última rodada
ultima_rodada = tabela_jacare[(tabela_jacare['rodada']==max_rodada)] #df da última rodada
p1 = int(ultima_rodada['pontos'].min()) #pontuação do 1o colocado
p2 = int(ultima_rodada['pontos'].max()) #pontuação máxima do 2o colocado
#titulo linha 1o colocado
fig3.add_annotation(x=max_rodada / 2, y=p1, #adicionando o label: x=max_rodada / 2 (meio do campeonado realizado)
            text='Pontuação do 1º colocado',
            showarrow=False,
            xshift=0,
            yshift=-20,
            font=dict(size=12, color=cores[0])
            )
#valor primeiro colocado
fig3.add_annotation(x=max_rodada, y=p1, #adicionando o label na última rodada: x=max_rodada
            text=str(p1),
            showarrow=False,
            xshift=20,
            yshift=0,
            font=dict(size=16, color=cores[0])
            )
#titulo 2o colocado
fig3.add_annotation(x=max_rodada / 2, y=p2,
            text='Pontuação máxima do 2º colocado',
            showarrow=False,
            xshift=0,
            yshift=20,
            font=dict(size=12, color=cores[1])
            )
#valor 2o colocado
fig3.add_annotation(x=max_rodada, y=p2,
            text=str(p2),
            showarrow=False,
            xshift=20,
            yshift=0,
            font=dict(size=16, color=cores[1])
            )
fig3.update_layout(showlegend=False)

col3.plotly_chart(fig3, use_container_width=True)

#cálculo de previsão do encontro das linhas
#p2 previsão de pontos do 2o colocado nas próximas rodadas
p2 = tabela_consolidada[(tabela_consolidada['rodada_projecao'] == max_rodada) & (tabela_consolidada['classificacao'] == 2)]
p2 = int(p2['media_pontos_total'].max() * (38 - p2['jogos_total'].max()))

#p1 número de rodadas que o lider precisa para atingir p2
p1 = tabela_consolidada[(tabela_consolidada['rodada_projecao'] == max_rodada) & (tabela_consolidada['classificacao'] == 1)]
no_jogos_lider = p1['jogos_total'].max()
p1 = int(p2 / p1['media_pontos_total'].max() + no_jogos_lider)

#indicador com o resultado do cálculo
fig4 = go.Figure()
fig4.add_trace(go.Indicator(
    mode='number',
    value=p1,
    title='Rodada de confirmação do título'
))
col4.plotly_chart(fig4, use_container_width=True)


#link
st.sidebar.link_button('Meu perfil no LinkedIn', 'https://www.linkedin.com/in/robertoschneider/')

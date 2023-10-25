# %% [markdown]
# ### Campeonato Brasileiro 2023
# ##### Projeção da classificação final do Campeonato Brasileiro 2023
# **Mémória de cálculo da projeção**<br>
# *mpm x prm + mpv x prv*<br>
# 
# ###### **mpm**: média de pontos como mandante;<br>**mpv**: média de pontos como visitante;<br>**prm**: partidas restantes como mandante;<br>**prv**: partidas restantes como visitante.
# 

# %%
#importação das biblioteca
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

pd.options.mode.chained_assignment = None

#carregando a tabela
tabela_completa = pd.read_csv('https://raw.githubusercontent.com/betoschneider/br23/main/tabela_br23.csv', sep=';')


#criando uma cópia para remover as partidas não realizadas
tabela = tabela_completa.copy()
tabela = tabela.dropna()

#numero de rodadas jogadas
max_rodada = tabela['rodada'].max()

# %%
#construindo historico de classificação
df_consolidado = None
tabela_consolidada = None
projecao_consolidada = None

for i in range(max_rodada):
    rodada = tabela[tabela['rodada']==i+1]

    #definindo resultado da partida
    rodada['vitoria_mandante'] = rodada.apply(lambda x: 1 if(x['gols_mandante'] > x['gols_visitante']) else 0, axis=1)
    rodada['vitoria_visitante'] = rodada.apply(lambda x: 1 if(x['gols_mandante'] < x['gols_visitante']) else 0, axis=1)
    rodada['empate'] = rodada.apply(lambda x: 1 if(x['gols_mandante'] == x['gols_visitante']) else 0, axis=1)

    #resumo
    #jogos como mandante
    df_mandante = rodada[['time_mandante', 'gols_mandante', 'gols_visitante', 'vitoria_mandante', 'empate', 'vitoria_visitante']]
    df_mandante.columns = ['time', 'gols_marcados_mandante', 'gols_sofridos_mandante', 'vitoria_mandante', 'empate_mandante', 'derrota_mandante']
    #total mandante
    df_mandante = df_mandante.groupby(by="time").sum().reset_index()
    #jogos como visitante
    df_visitante = rodada[['time_visitante', 'gols_visitante', 'gols_mandante', 'vitoria_visitante', 'empate', 'vitoria_mandante']]
    df_visitante.columns = ['time', 'gols_marcados_visitante', 'gols_sofridos_visitante', 'vitoria_visitante', 'empate_visitante', 'derrota_visitante']
    #total visitante
    df_visitante = df_visitante.groupby(by="time").sum().reset_index()

    #consolidando os dados
    df_consolidado = pd.concat([df_consolidado, pd.concat([df_mandante, df_visitante], ignore_index=True)], ignore_index=True)
    df_consolidado = df_consolidado.groupby(by="time").sum().reset_index()
    #numeros consolidados
    df_consolidado['jogos_mandante'] = df_consolidado['vitoria_mandante'] + df_consolidado['empate_mandante'] + df_consolidado['derrota_mandante']
    df_consolidado['jogos_visitante'] = df_consolidado['vitoria_visitante'] + df_consolidado['empate_visitante'] + df_consolidado['derrota_visitante']
    df_consolidado['jogos_total'] = df_consolidado['jogos_mandante'] + df_consolidado['jogos_visitante']
    df_consolidado['vitoria_total'] = df_consolidado['vitoria_mandante'] + df_consolidado['vitoria_visitante']
    df_consolidado['empate_total'] = df_consolidado['empate_mandante'] + df_consolidado['empate_visitante']
    df_consolidado['derrota_total'] = df_consolidado['derrota_mandante'] + df_consolidado['derrota_visitante']
    df_consolidado['pontos_mandante'] = df_consolidado['vitoria_mandante'] * 3 + df_consolidado['empate_mandante']
    df_consolidado['media_pontos_mandante'] = df_consolidado['pontos_mandante'] / (df_consolidado['vitoria_mandante'] + df_consolidado['empate_mandante'] + df_consolidado['derrota_mandante'])
    df_consolidado['pontos_visitante'] = df_consolidado['vitoria_visitante'] * 3 + df_consolidado['empate_visitante']
    df_consolidado['media_pontos_visitante'] = df_consolidado['pontos_visitante'] / (df_consolidado['vitoria_visitante'] + df_consolidado['empate_visitante'] + df_consolidado['derrota_visitante'])
    df_consolidado['pontos_total'] = df_consolidado['pontos_mandante'] + df_consolidado['pontos_visitante']
    df_consolidado['media_pontos_total'] = df_consolidado['pontos_total'] / (df_consolidado['vitoria_total'] + df_consolidado['empate_total'] + df_consolidado['derrota_total'])
    df_consolidado['aproveitamento_mandante'] = df_consolidado['pontos_mandante'] / (df_consolidado['jogos_mandante'] * 3)
    df_consolidado['aproveitamento_visitante'] = df_consolidado['pontos_visitante'] / (df_consolidado['jogos_visitante'] * 3)
    df_consolidado['aproveitamento_total'] = df_consolidado['pontos_total'] / (df_consolidado['jogos_total'] * 3)
    df_consolidado['gols_marcados_total'] = df_consolidado['gols_marcados_mandante'] + df_consolidado['gols_marcados_visitante']
    df_consolidado['saldo_gols_mandante'] = df_consolidado['gols_marcados_mandante'] - df_consolidado['gols_sofridos_mandante']
    df_consolidado['saldo_gols_visitante'] = df_consolidado['gols_marcados_visitante'] - df_consolidado['gols_sofridos_visitante']
    df_consolidado['saldo_gols_total'] = df_consolidado['saldo_gols_mandante'] + df_consolidado['saldo_gols_visitante']
    #ordenando a tabela consolidada
    df_consolidado.sort_values(by=['pontos_total', 'vitoria_total', 'saldo_gols_total', 'gols_marcados_total'], ascending=False, inplace=True)
    df_consolidado = df_consolidado.reset_index().reset_index()
    df_consolidado['classificacao'] = df_consolidado['level_0'] + 1
    df_consolidado.drop(columns=['level_0', 'index'], inplace=True)

    df_consolidado = df_consolidado[['classificacao', 'time', 'pontos_total', 'jogos_total', 'vitoria_total', 'empate_total', 'derrota_total', 
                                    'gols_marcados_total', 'saldo_gols_total', 'media_pontos_total', 'aproveitamento_total', 'pontos_mandante',
                                    'jogos_mandante', 'vitoria_mandante', 'empate_mandante', 'derrota_mandante', 'gols_marcados_mandante', 'gols_sofridos_mandante',
                                    'saldo_gols_mandante', 'media_pontos_mandante', 'aproveitamento_mandante', 'pontos_visitante', 'jogos_visitante', 'vitoria_visitante', 
                                    'empate_visitante', 'derrota_visitante', 'gols_marcados_visitante', 'gols_sofridos_visitante', 'saldo_gols_visitante', 
                                    'media_pontos_visitante','aproveitamento_visitante']]
    
    #historico de classificação na tabela consolidada
    #tabela_consolidada = pd.concat([tabela_consolidada, df_consolidado], ignore_index=True)

    #projecao
    df_consolidado['jogos_mandante_restante'] = 19 - df_consolidado['jogos_mandante']
    df_consolidado['jogos_visitante_restante'] = 19 - df_consolidado['jogos_visitante']
    df_consolidado['pontos_projetados'] = round(df_consolidado['jogos_mandante_restante'] * df_consolidado['media_pontos_mandante'] + df_consolidado['jogos_visitante_restante'] * df_consolidado['media_pontos_visitante'], 0)
    df_consolidado['pontos_finais'] = df_consolidado['pontos_projetados'] + df_consolidado['pontos_total']
    df_consolidado.sort_values(by='pontos_finais', ascending=False, inplace=True)
    df_consolidado = df_consolidado.reset_index().reset_index()
    df_consolidado['classificacao'] = df_consolidado['level_0'] + 1
    df_consolidado.drop(columns=['level_0', 'index'], inplace=True)
    df_consolidado['rodada_projecao'] = i + 1

    #historico de classificação na tabela consolidada
    tabela_consolidada = pd.concat([df_consolidado, tabela_consolidada], ignore_index=True)




# %%
#projecao na rodada mais recente
ultima_projecao = tabela_consolidada[tabela_consolidada['rodada_projecao'] == max_rodada]
ultima_projecao = ultima_projecao[['classificacao', 'time', 'pontos_finais']]

# %%
#visualização

######################################
#                                    #
# criando um dashboard com streamlit #
#                                    #
######################################

#configurando o layout de página
st.set_page_config(layout='wide')

#título
st.write('''
    ### Campeonato Brasileiro 2023
    ##### Projeção da classificação final do Campeonato Brasileiro 2023
    '''
)

#filtros
time = st.sidebar.selectbox('Time', tabela_consolidada['time'].unique())
tabela_consolidada_filtro = tabela_consolidada[(tabela_consolidada['time']==time) & (tabela_consolidada['rodada_projecao']==max_rodada)]

#colunas na página
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# %%

#cores das linhas e barras
cores = px.colors.qualitative.Pastel + px.colors.qualitative.Pastel1

#grafico 2: historico projecao
fig2 = px.line(tabela_consolidada, x='rodada_projecao', y='pontos_finais', color='time',
               title='Projeção final rodada a rodada', 
               color_discrete_sequence=cores
               )
col1.plotly_chart(fig2, use_container_width=True)
#grafico 1: projecao final
fig1 = px.bar(tabela_consolidada[tabela_consolidada['rodada_projecao'] == max_rodada], x='pontos_finais', y='time', color='time', 
              title='Projeção atual', orientation='h', 
              text='pontos_finais',
              color_discrete_sequence=cores
              )
fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False) #rótulo de dados da barra
fig1.update_yaxes(tickfont_size=11) #tamanho da fonte do rótulo do eixo y
fig1.update_layout(showlegend=False)

#tabela_consolidada[df_consolidado['rodada_projecao'] == max_rodada]
col2.plotly_chart(fig1, use_container_width=True)

#resultado por time
col3.write('# %s' % (time) + '''

''' + 'Realizado até a rodada ' + str(max_rodada)
, use_container_width=True)

col4.write('####  ' + '''

''' + 
str(int(tabela_consolidada_filtro['classificacao'].max())) + 'º lugar' + '''

''' +
str(int(tabela_consolidada_filtro['vitoria_total'].max())) + 'v ' + 
str(int(tabela_consolidada_filtro['empate_total'].max())) + 'e ' + 
str(int(tabela_consolidada_filtro['derrota_total'].max())) + 'd' + '''

''' +
str(int(tabela_consolidada_filtro['pontos_total'].max())) + ' pontos' + ' (' + str(round(tabela_consolidada_filtro['media_pontos_total'].max(), 2)) + ' pontos por jogo)' + '''

''' +
str(round(tabela_consolidada_filtro['aproveitamento_total'].max() * 100, 2)) + '% de aproveitamento'
, use_container_width=True)

col5.write('####  ' + '''

''' +
str(int(tabela_consolidada_filtro['gols_marcados_total'].max())) + ' gols marcados' + '''

''' + 
str(int(tabela_consolidada_filtro['saldo_gols_total'].max())) + ' gols de saldo'
, use_container_width=True)



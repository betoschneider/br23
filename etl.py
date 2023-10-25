

class ETL:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        pass

    def get_tabela(self):
        import pandas as pd
        pd.options.mode.chained_assignment = None

                
        #carregando a tabela
        tabela_completa = pd.read_csv(self.arquivo, sep=';')

        #criando uma cópia para remover as partidas não realizadas
        tabela = tabela_completa.copy()
        tabela = tabela.dropna()

        #numero de rodadas jogadas
        max_rodada = tabela['rodada'].max()

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

        df_consolidado = None
        df_mandante = None
        df_visitante = None
        tabela = None
        tabela_completa = None
        return tabela_consolidada

if __name__ == '__main__':
    #para testar a classe
    arquivo = 'https://raw.githubusercontent.com/betoschneider/br23/main/tabela_br23.csv'
    base = ETL(arquivo)
    tabela_consolidada = base.get_tabela()
    print(tabela_consolidada.head())

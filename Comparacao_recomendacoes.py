import pandas as pd
import numpy as np 
from csv import reader
import constants



def experimento_online(grupo):

    # Retorna um dataframe com os locais avaliados pelos grupos na recomendação online (experimento 1)

    diretorio = './recomendacoes_geradas/recomendacoes_1online/' + str(grupo)+ '.csv'

    cols = [1,2,3,4,8,9,10]    
    cols = [1,2,3,4]   
    cols = [0,1,2,3]
    df_online = pd.read_csv(diretorio, low_memory=False)
    df_online = df_online.drop(df_online.columns[cols],axis=1)

    # dropping todos os valores duplicados
    df_online.sort_values("Nome", inplace = True)
    df_online.drop_duplicates(subset ="Nome", keep = False, inplace = True)


    return df_online

def comparacao_online__standard(metodos, grupo, df_online):

    for aux in metodos:
        diretorio = constants.DATA_STANDARD + str(grupo) + '_std_' + aux + '.csv'

        print('STANDARD - METODO ' +  aux + ' STANDARD')

        # Compara as avaliações online com a recomendação standard
        df_standard = pd.read_csv(diretorio, names=['Posicao','PoiId','Nome','Categoria', 'Endereco'], skiprows=3, nrows=10)
        merged_standard = df_standard.merge(df_online[['Discussão', 'Nome']], on=['Nome'], how='left')


        # Calcula o MRR
        merged_standard['MRR'] = 1/merged_standard['Posicao']
        merged_standard['Tecnica'] = 'Standard ' + str(aux)

        print(merged_standard)

        # Compara as avaliações online com a recomendação standard diversificada
        print('\nSTANDARD - METODO ' +  aux + ' DIVERSIFICADO')
        df_diversificado = pd.read_csv(diretorio, names=['Posicao','PoiId','Nome','Categoria', 'Endereco'], skiprows=15, nrows=25)
        merged_diversificado = df_diversificado.merge(df_online[['Discussão', 'Nome']], on=['Nome'], how='left')


        # Calcula o MRR
        merged_diversificado['MRR'] = (1/merged_diversificado['Posicao'])
        merged_diversificado['Tecnica'] = (aux + ' Diversificado')

        print(merged_diversificado)

        print('\n')

        # Salva as recomendações já com as notas das avaliações online
        ''' merged_standard.to_csv(constants.DATA_COMPARACOES + str(grupo) + '_std_' + aux +'.csv', index = False, header = True)
        merged_diversificado.to_csv(constants.DATA_COMPARACOES + str(grupo) + '_std_' + aux +'.csv', mode='a', index = False, header = True)'''

        #save_xsls(grupo, merged_standard, merged_diversificado, aux, 'std')
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(constants.DATA_COMPARACOES + str(grupo)+'_std_'+  aux +'.xlsx', engine='xlsxwriter')
        # Write each dataframe to a different worksheet.
        merged_standard.to_excel(writer, sheet_name=aux)
        merged_diversificado.to_excel(writer, sheet_name=aux+'_diversificado')
        writer.save()

def comparacao_online__distancia(metodos, grupo, df_online):

    for aux in metodos:
        diretorio = constants.DATA_DISTANCIA + str(grupo) + '_dist_' + aux + '.csv'

        print('DISTANCIA - METODO ' +  aux + ' STANDARD')

        # Compara as avaliações online com a recomendação standard
        df_standard = pd.read_csv(diretorio, names=['Posicao','PoiId','Nome','Categoria', 'Endereco'], skiprows=3, nrows=10)
        merged_standard = df_standard.merge(df_online[['Discussão', 'Nome']], on=['Nome'], how='left')


        # Calcula o MRR
        merged_standard['MRR'] = 1/merged_standard['Posicao']
        merged_standard['Tecnica'] = 'Distancia ' + str(aux)

        print(merged_standard)

        # Compara as avaliações online com a recomendação standard diversificada
        print('\nDISTANCIA - METODO ' +  aux + ' DIVERSIFICADO')
        df_diversificado = pd.read_csv(diretorio, names=['Posicao','PoiId','Nome','Categoria', 'Endereco'], skiprows=15, nrows=25)
        merged_diversificado = df_diversificado.merge(df_online[['Discussão', 'Nome']], on=['Nome'], how='left')


        # Calcula o MRR
        merged_diversificado['MRR'] = (1/merged_diversificado['Posicao'])
        merged_diversificado['Tecnica'] = ('Distancia ' + aux + ' Diversificado')

        print(merged_diversificado)

        print('\n')

        # Salva as recomendações já com as notas das avaliações online
        '''merged_standard.to_csv(constants.DATA_COMPARACOES + str(grupo) + '_dist_' + aux +'.csv', index = False, header = True)
        merged_diversificado.to_csv(constants.DATA_COMPARACOES + str(grupo) + '_dist_' + aux +'.csv', mode='a', index = False, header = True)'''

        #save_xsls(grupo, merged_standard, merged_diversificado, aux, 'dist')

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(constants.DATA_COMPARACOES + str(grupo)+'_dist_'+  aux +'.xlsx', engine='xlsxwriter')

        # Write each dataframe to a different worksheet.
        merged_standard.to_excel(writer, sheet_name=aux)
        merged_diversificado.to_excel(writer, sheet_name=aux +'_diversificado')
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()


def comparacao_online__preferencia(metodos, grupo, df_online):

    for aux in metodos:
        diretorio = constants.DATA_PREFERENCIA + str(grupo) + '_pref_' + aux + '.csv'

        print('PREFERENCIA - METODO ' +  aux + ' STANDARD')

        # Compara as avaliações online com a recomendação standard
        df_standard = pd.read_csv(diretorio, names=['Posicao','PoiId','Nome','Categoria', 'Endereco'], skiprows=3, nrows=10)
        merged_standard = df_standard.merge(df_online[['Discussão', 'Nome']], on=['Nome'], how='left')


        # Calcula o MRR
        merged_standard['MRR'] = 1/merged_standard['Posicao']
        merged_standard['Tecnica'] = 'Preferencia ' + str(aux)

        print(merged_standard)

        # Compara as avaliações online com a recomendação standard diversificada
        print('\nPREFERENCIA - METODO ' +  aux + ' DIVERSIFICADO')
        df_diversificado = pd.read_csv(diretorio, names=['Posicao','PoiId','Nome','Categoria', 'Endereco'], skiprows=15, nrows=25)
        merged_diversificado = df_diversificado.merge(df_online[['Discussão', 'Nome']], on=['Nome'], how='left')


        # Calcula o MRR
        merged_diversificado['MRR'] = (1/merged_diversificado['Posicao'])
        merged_diversificado['Tecnica'] = ('Preferencia ' + aux + ' Diversificado')

        print(merged_diversificado)

        print('\n')

        # Salva as recomendações já com as notas das avaliações online
        '''merged_standard.to_csv(constants.DATA_COMPARACOES + str(grupo) + '_pref_' + aux +'.csv', index = False, header = True)
        merged_diversificado.to_csv(constants.DATA_COMPARACOES + str(grupo) + '_pref_' + aux +'.csv', mode='a', index = False, header = True)'''

        #save_xsls(grupo, merged_standard, merged_diversificado, aux, 'pref')

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(constants.DATA_COMPARACOES + str(grupo)+'_pref_'+  aux +'.xlsx', engine='xlsxwriter')

        # Write each dataframe to a different worksheet.
        merged_standard.to_excel(writer, sheet_name=aux)
        merged_diversificado.to_excel(writer, sheet_name=aux +'_diversificado')
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()




grupo = [864, 854, 844]

metodos = ['AWM', 'AV','LM']
df_online = experimento_online(grupo)
comparacao_online__standard(metodos, grupo, df_online)
print('------------------------------------------------------------------------------------------------------------------------------------------------')
comparacao_online__distancia(metodos, grupo, df_online)
print('------------------------------------------------------------------------------------------------------------------------------------------------')
comparacao_online__preferencia(metodos, grupo, df_online)
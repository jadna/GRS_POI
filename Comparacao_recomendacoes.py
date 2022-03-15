from logging import NullHandler
import pandas as pd
import numpy as np 
from csv import reader


# Online são as recomendações avaliadas pelos grupos no experimento ONLINE
DATA_ONLINE = './recomendacoes_geradas/recomendacoes_1online/'
DATA_STANDARD = './recomendacoes_geradas/recomendacoes_standard/Grupos_3/'
DATA_DISTANCIA = './recomendacoes_geradas/recomendacoes_distancia/Grupos_3/'
DATA_PREFERENCIA = './recomendacoes_geradas/recomendacoes_preferencia/Grupos_3/'
DATA_COMPARACOES = './recomendacoes_geradas/recomendacoes_comparadas_online/Grupos_3/'

def experimento_online(grupo):

    # Retorna um dataframe com os locais avaliados pelos grupos na recomendação online (experimento 1)

    diretorio = './recomendacoes_geradas/recomendacoes_1online/' + str(grupo)+ '.csv'

    cols = [1,2,3,4,8,9,10]    
    cols = [1,2,3,4]   
    df_online = pd.read_csv(diretorio, low_memory=False)
    df_online = df_online.drop(df_online.columns[cols],axis=1)

    # dropping todos os valores duplicados
    df_online.sort_values("Nome", inplace = True)
    df_online.drop_duplicates(subset ="Nome", keep = False, inplace = True)


    return df_online

def comparacao_online__standard(metodos, grupo, df_online):

    for aux in metodos:
        diretorio = DATA_STANDARD + str(grupo) + '_std_' + aux + '.csv'

        print('STANDARD - METODO ' +  aux)

        # Compara as avaliações online com a recomendação standard
        print('---------------------------------------------------- STANDARD ----------------------------------------------------')
        df_standard = pd.read_csv(diretorio, names=['Posicao','PoiId','Nome','Categoria', 'Endereco'], skiprows=3, nrows=10)
        merged_standard = df_standard.merge(df_online[['Discussão', 'Nome']], on=['Nome'], how='left')


        if merged_standard['Discussão'].empty:
            merged_standard['MRR'] = (1/merged_standard['Posicao'])
        
        merged_standard['Tecnica'] = 'Standard ' + aux

        print(merged_standard)

        # Compara as avaliações online com a recomendação standard diversificada
        print('---------------------------------------------------- DIVERSIFICADO ----------------------------------------------------')
        df_diversificado = pd.read_csv(diretorio, names=['Posicao','PoiId','Nome','Categoria', 'Endereco'], skiprows=15, nrows=25)
        merged_diversificado = df_diversificado.merge(df_online[['Discussão', 'Nome']], on=['Nome'], how='left')

        if merged_diversificado['Discussão'].empty:
            merged_diversificado['MRR'] = (1/merged_diversificado['Posicao'])
        

        merged_diversificado['Tecnica'] = (aux + ' Diversificado')

        print(merged_diversificado)

        print('\n')


        # Salva as recomendações já com as notas das avaliações online
        merged_standard.to_csv(DATA_COMPARACOES + str(grupo) + '_std_' + aux +'.csv', index = False, header = True)
        merged_diversificado.to_csv(DATA_COMPARACOES + str(grupo) + '_std_' + aux +'.csv', mode='a', index = False, header = True)

        save_xsls(grupo, merged_standard, merged_diversificado, aux, 'std')

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(DATA_COMPARACOES + str(grupo)+'_std_'+  aux +'.xlsx', engine='xlsxwriter')

        # Write each dataframe to a different worksheet.
        merged_standard.to_excel(writer, sheet_name=aux)
        merged_diversificado.to_excel(writer, sheet_name=aux+'_diversificado')
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

def comparacao_online__distancia(metodos, grupo, df_online):

    for aux in metodos:
        diretorio = DATA_DISTANCIA + str(grupo) + '_dist_' + aux + '.csv'

        print('DISTANCIA - METODO ' +  aux)

        # Compara as avaliações online com a recomendação distancia standard
        print('---------------------------------------------------- STANDARD ----------------------------------------------------')
        df_standard = pd.read_csv(diretorio, names=['Posicao','PoiId','Nome','Categoria', 'Endereco'], skiprows=3, nrows=10)
        merged_standard = df_standard.merge(df_online[['Discussão', 'Nome']], on=['Nome'], how='left')
        merged_standard = merged_standard.fillna(0)

        if merged_standard['Discussão'].empty:
            print(merged_standard['Discussão'].empty)
            merged_standard['MRR'] = (1/merged_standard['Posicao'])

        merged_standard['Tecnica'] = 'Distancia ' + aux

        print(merged_standard)

        # Compara as avaliações online com a recomendação standard diversificada
        print('---------------------------------------------------- DIVERSIFICADO ----------------------------------------------------')
        df_diversificado = pd.read_csv(diretorio, names=['Posicao','PoiId','Nome','Categoria', 'Endereco'], skiprows=15, nrows=25)
        merged_diversificado = df_diversificado.merge(df_online[['Discussão', 'Nome']], on=['Nome'], how='left')

        if not merged_diversificado['Discussão'].empty:
            merged_diversificado['MRR'] = (1/merged_diversificado['Posicao'])
        
        merged_diversificado['Tecnica'] = 'Distancia ' + aux + ' Diversificado'
        print(merged_diversificado)


        # Salva as recomendações já com as notas das avaliações online
        merged_standard.to_csv(DATA_COMPARACOES + str(grupo) + '_dist_' + aux +'.csv', index = False, header = True)
        merged_diversificado.to_csv(DATA_COMPARACOES + str(grupo) + '_dist_' + aux +'.csv', mode='a', index = False, header = True)
        save_xsls(grupo, merged_standard, merged_diversificado, aux, 'dist')


def comparacao_online__preferencia(metodos, grupo, df_online):

    for aux in metodos:
        diretorio = DATA_PREFERENCIA + str(grupo) + '_pref_' + aux + '.csv'

        print('PREFERENCIA - METODO ' +  aux)

        # Compara as avaliações online com a recomendação preferencia standard
        print('---------------------------------------------------- STANDARD ----------------------------------------------------')
        df_standard = pd.read_csv(diretorio, names=['Posicao','PoiId','Nome','Categoria', 'Endereco'], skiprows=3, nrows=10)
        merged_standard = df_standard.merge(df_online[['Discussão', 'Nome']], on=['Nome'], how='left')
       
        if merged_standard['Discussão'].empty:
            merged_standard['MRR'] = (1/merged_standard['Posicao'])
        else: 
            merged_standard['MRR'] = 0

        merged_standard['Tecnica'] = 'Preferencia ' + aux
        print(merged_standard)

        # Compara as avaliações online com a recomendação standard diversificada
        print('---------------------------------------------------- DIVERSIFICADO ----------------------------------------------------')
        df_diversificado = pd.read_csv(diretorio, names=['Posicao','PoiId','Nome','Categoria', 'Endereco'], skiprows=15, nrows=25)
        merged_diversificado = df_diversificado.merge(df_online[['Discussão', 'Nome']], on=['Nome'], how='left')

        if merged_diversificado['Discussão'].empty:
            merged_diversificado['MRR'] = (1/merged_diversificado['Posicao'])
        else: 
            merged_diversificado['MRR'] = 0

        merged_diversificado['Tecnica'] = 'Preferencia ' + aux + ' Diversificado'
        print(merged_diversificado)
        print('\n')

        # Salva as recomendações já com as notas das avaliações online
        merged_standard.to_csv(DATA_COMPARACOES + str(grupo) + '_pref_' + aux +'.csv', index = False, header = True)
        merged_diversificado.to_csv(DATA_COMPARACOES + str(grupo) + '_pref_' + aux +'.csv', mode='a', index = False, header = True)

        save_xsls(grupo, merged_standard, merged_diversificado, aux, 'pref')


def save_xsls(grupo, df1, df2, metodo, tipo):

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(DATA_COMPARACOES + str(grupo)+'.xlsx', engine='xlsxwriter')

    # Write each dataframe to a different worksheet.
    df1.to_excel(writer, sheet_name=tipo+'_'+metodo)
    df2.to_excel(writer, sheet_name=tipo+'_'+metodo+'_diversificado')


    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

grupo = [254,314,324]

metodos = ['AWM', 'AV','LM']
df_online = experimento_online(grupo)
comparacao_online__standard(metodos, grupo, df_online)
comparacao_online__distancia(metodos, grupo, df_online)
comparacao_online__preferencia(metodos, grupo, df_online)
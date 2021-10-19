import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.dtypes.missing import isnull
import plotly.express as px
import plotly.graph_objects as go
import sys
import platform as pl
from geopy.distance import great_circle
import datetime 
import time

from traitlets.traitlets import Int

# coords_1 = (-3.944121,-38.71891)
# coords_2 = (-3.944121,-38.718906)
# print(great_circle(coords_1, coords_2).m)

# pesos = np.array([850,600,750,1050,1150,800])
# conchada = lambda x:x[np.random.choice(x.shape[0],1, replace=False)][0]

def conchada():
    pesos = np.array([850,600,750,1050,1150,800])
    return pesos[np.random.choice(pesos.shape[0],1, replace=False)][0]


class dataObject():
    def __init__(self, name):
        sep = '\\' if pl.uname().system == 'Windows' else '/'
        self.df = pd.read_csv(f"dados{sep}{name}", encoding='iso-8859-1')
        if len(self.df.columns) > 9:
            self.df = self.df.iloc[:,1:]
        self.df.columns = ["latitude", "longitude", "status", "angle", "fuel", "weight", "velocity", "imei", "date_created"]
        # Remove linhas inválidas
        self.df.dropna(0, inplace=True)
        # Ordena pela data
        self.df.sort_values('date_created', inplace=True)
        self.gps = self.df.loc[self.df['latitude'] < -1, ['latitude','longitude']].values
        self.df_filtered = self.df.loc[self.df['latitude'] < -1]
        self.gps_data = tuple(zip(self.df['latitude'].values, self.df['longitude'].values))


    def saveDataFrame(self, name_file):
        self.df_filtered.to_csv(name_file)


    """
        datas: um dataframe com duas colunas, sendo latitude e longitude, respectivamente.
    """
    @classmethod
    def plotDatas(cls, fig, datas, is_line=True, label=''):
        if fig is None:
            fig = go.Figure(go.Scattermapbox(
            mode = "markers+lines" if is_line == True else "markers",
            lon = datas[:,1],
            lat = datas[:,0],
            text = label if label != '' else 'veic1',
            marker = {'size': 10,
                    'color': 'blue'}))
        else:
            fig.add_trace(go.Scattermapbox(
            mode = "markers+lines" if is_line == True else "markers",
            lon = datas[:,1],
            lat = datas[:,0],
            text = label if label != '' else 'veic2',
            marker = {'size': 10,
                    'color': 'red'}))    

        fig.update_layout(
            margin ={'l':0,'t':0,'b':0,'r':0},
            #'center': {'lon': -38.71901, 'lat':  -3.94467},
            mapbox = {
                'center': {'lon': datas[:,1].mean(), 'lat':  datas[:,0].mean()},
                'style': "stamen-terrain",
                'center': {'lon': datas[:,1].mean(), 'lat':  datas[:,0].mean()},
                'zoom': 16})
        return fig


    """
        Convert data em timestamp Unix.
        Exemplo: df_filtered['timestamp'] = dataObject.convertToTimestamp(df_filtered['date_created'])
    """
    @classmethod
    def convertToTimestamp(cls, datetime_data):
        dates = pd.to_datetime(datetime_data)
        return (dates - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

    @classmethod
    def mergeDataFrames(cls, df1, df2):
        df_merged = [df1, df2]
        df_merged = pd.concat(df_merged)
        return df_merged


    """
        Adiciona um deslocamento de tempo em minutos.
        df_time: coluna do dataframe do tipo string de datetime.
        minutes: minutos desejados a deslocar.
        retorna: coluna de dataframe com tempo deslocado
        Exemplo: esc.df_filtered['offset'] = dataObject.addOffset(esc.df_filtered['date_created'], -3) 
    """
    @classmethod
    def addOffset(cls, df_time, minutes):
        return pd.to_datetime(df_time.values) + pd.to_timedelta(minutes, unit='m')

    
    """
        Cria um intervalo de amostragem no índice do dataframe e agrupa as demais variáveis por sua média. 
        Este método irá alterar a estrutura do dataframe.
        interval: intervalo em segundos.
    """
    @classmethod
    def normalizeInterval(self, df, interval, drop_null = True):
        interval = f'{int(interval)}s'
        df.loc[:,'date_created'] = pd.to_datetime(df['date_created'])
        df.loc[:,'index'] = pd.DatetimeIndex(df['date_created'].values)
        # offset_time = datetime.timedelta(minutes = 7)
        df = df.groupby(pd.Grouper(key='index',freq=interval, label='right', sort=True)).mean()
        # df = df.resample()
        if drop_null:
            df = df.dropna()
        return df


if __name__ == "__main__": 

    file_esc = 'logs_escavadeira_18_08_21_filtered.csv'
    file_cam = 'logs_Caminhao_17_08_21_filtered.csv'

    esc = dataObject(file_esc)
    cam_ant = dataObject(file_cam)
    fig1 = None

    # Distância em metros entre os dois veículos
    DISTANCE = 5
    # Intervalo em segundos da normalização
    INTERVAL_TIME = 10

    # Normaliza intervalos em INTERVAL_TIME e substitui valores NaN por -1
    esc.df_filtered = dataObject.normalizeInterval(esc.df_filtered, interval = INTERVAL_TIME, drop_null=False).fillna(-1)
    cam_ant.df_filtered = dataObject.normalizeInterval(cam_ant.df_filtered, interval = INTERVAL_TIME, drop_null=False).fillna(-1)

    # Define Janela de tempo 
    esc.df_ready = esc.df_filtered.loc['2021-08-06 12:15:00':'2021-08-17 07:44:00']
    cam_ant.df_ready = cam_ant.df_filtered.loc['2021-08-06 12:15:00':'2021-08-17 07:44:00']

    # Cria um novo dataframe incluindo dados de ambos os veículos
    df_datas = esc.df_ready.copy()
    df_datas['velocity_cam'] = cam_ant.df_ready['velocity']
    df_datas['latitude_cam'] = cam_ant.df_ready['latitude']
    df_datas['longitude_cam'] = cam_ant.df_ready['longitude']

    # Filtra os dados de geolocalização válidos de ambos os veículos
    df_datas_fil = df_datas.loc[(df_datas['latitude'] < -1) & (df_datas['latitude_cam'] < -1)]

    # Calcula Intervalo entre dois pontos geográficos
    esc_values = df_datas_fil.loc[:, ['latitude', 'longitude']].values
    cam_values = df_datas_fil.loc[:, ['latitude_cam', 'longitude_cam']].values
    distance = np.array([])

    for i, esc_val in enumerate(esc_values):
        try:
            distance = np.append(distance, great_circle(esc_val, cam_values[i]).m)
        except:
            distance = np.append(distance, 1000)


    df_datas_fil['distance'] = distance
    print(df_datas_fil.loc[df_datas_fil['distance'] < DISTANCE])
    print('\nCAM_ANT:\n')
    # print(cam_ant.df_filtered.loc['2021-08-06 12:53:00':'2021-08-06 13:13:20'].head())
    cam_desc = cam_ant.df_filtered.loc['2021-08-06 12:53:00':'2021-08-06 13:13:20']
    print(df_datas_fil.loc[df_datas_fil['weight'] > 0])
    # print(df_datas_fil.loc[df_datas_fil['distance'] < DISTANCE])
    # sys.exit()
    # # Geracao Grafico
    esc_fil = df_datas_fil.loc[df_datas_fil['weight'] > 0, ['latitude','longitude']]
    # esc_fil = df_datas_fil.loc[df_datas_fil['distance'] < DISTANCE, ['latitude','longitude']]
    # cam_fil = df_datas_fil.loc[df_datas_fil['distance'] < DISTANCE, ['latitude_cam','longitude_cam']]
    # esc_fil = esc.df_filtered.loc[esc.df_filtered['velocity'].astype(float) < 1, ['latitude','longitude']]
    # cam_fil = cam_ant.df_filtered.loc[cam_ant.df_filtered['velocity'].astype(float) < 1, ['latitude','longitude']]
    fig1 = dataObject.plotDatas(fig1, esc_fil.values, is_line=False, label='escavadeira')
    # fig1 = dataObject.plotDatas(fig1, cam_fil.values, is_line=False, label='caminhao')
    fig1.show()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.dtypes.missing import isnull
import plotly.express as px
import plotly.graph_objects as go
import sys
import platform as pl
from geopy.distance import great_circle
from datetime import datetime
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
            mapbox = {
                'center': {'lon': -38.71901, 'lat':  -3.94467},
                'style': "stamen-terrain",
                'center': {'lon': -38.71901, 'lat': -3.94467},
                'zoom': 15})
        return fig


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
        df = df.groupby(pd.Grouper(key='index',freq=interval, origin='2021-08-06', offset='12h15min', sort=True)).mean()
        # df = df.resample()
        if drop_null:
            df = df.dropna()
        return df




if __name__ == "__main__": 

    file_cam = 'logs_caminhao_18_08_21_filtered.csv'
    file_esc = 'logs_escavadeira_18_08_21_filtered.csv'
    file = 'logs_Caminhao_17_08_21_filtered.csv'
    # cam = dataObject(file_cam)
    esc = dataObject(file_esc)
    cam_ant = dataObject(file)
    fig1 = None

    esc.df_filtered['timestamp'] = dataObject.convertToTimestamp(esc.df_filtered['date_created'])
    # Normaliza intervalos em 10s
    esc.df_filtered = dataObject.normalizeInterval(esc.df_filtered, interval = 10, drop_null=True)
    cam_ant.df_filtered = dataObject.normalizeInterval(cam_ant.df_filtered, interval = 10, drop_null=True)
    print(esc.df_filtered.head())
    print(cam_ant.df_filtered.head())

    # esc_gps_fil = esc.df_filtered.loc[:,['latitude','longitude']]
    # esc_gps_fil_values = esc_gps_fil.values


    # esc_fil = esc.df_filtered.loc[esc.df_filtered['velocity'].astype(float) < 1, ['latitude','longitude']]
    # fig1 = dataObject.plotDatas(fig1, esc_fil.values, is_line=False, label='escavadeira')
    # fig1.show()
    # # Geracao Grafico
    # esc_fil = esc.df_filtered.loc[esc.df_filtered['velocity'].astype(float) < 1, ['latitude','longitude']]
    # cam_fil = cam_ant.df_filtered.loc[cam_ant.df_filtered['velocity'].astype(float) < 1, ['latitude','longitude']]
    # fig1 = dataObject.plotDatas(fig1, esc_fil.values, is_line=False, label='escavadeira')
    # fig1 = dataObject.plotDatas(fig1, cam_fil.values, is_line=False, label='caminhao')
    # fig1.show()
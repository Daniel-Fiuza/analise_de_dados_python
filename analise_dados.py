import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import sys
import platform as pl
from geopy.distance import great_circle
from datetime import datetime
import time

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



file_cam = 'logs_caminhao_18_08_21_filtered.csv'
file_esc = 'logs_escavadeira_18_08_21_filtered.csv'
file = 'logs_Caminhao_17_08_21_filtered.csv'
# cam = dataObject(file_cam)
esc = dataObject(file_esc)
cam_ant = dataObject(file)


esc_gps_fil = esc.df_filtered.loc[:,['latitude','longitude']]
esc_gps_fil_values = esc_gps_fil.values
esc.df_filtered['timestamp'] = dataObject.convertToTimestamp(esc.df_filtered['date_created'])
esc_fil = esc.df_filtered.loc[esc.df_filtered['velocity'].astype(float) < 1, ['latitude','longitude']]
fig1 = None
fig1 = dataObject.plotDatas(fig1, esc_fil.values, is_line=False, label='escavadeira')
cam_fil = cam_ant.df_filtered.loc[cam_ant.df_filtered['velocity'].astype(float) < 1, ['latitude','longitude']]
fig1 = dataObject.plotDatas(fig1, cam_fil.values, is_line=False, label='caminhao')
fig1.show()
sys.exit()
cam_ant.df_filtered['date_time'] = cam_ant.df_filtered['date_created']
print(cam_ant.df_filtered['date_time'].values)
sys.exit()
cam_ant.df_filtered.plot(y='date_time')
sys.exit()
print(esc.df_filtered[great_circle(cam_ant.gps[13],esc_gps_fil).m < 6])
sys.exit()

for i in range(len(esc_gps_fil_values)):
    if great_circle(cam_ant.gps[13],esc_gps_fil_values[i]).m < 6:
        # print(f'coo_cam: {cam_ant.gps[13]}, coo_esc: {esc_gps_fil_values[i]}, idx_esc: {esc.df_filtered.index[i]}, dist: {great_circle(cam_ant.gps[13],esc_gps_fil_values[i]).m}, details:\n {esc.df_filtered.loc[esc.df_filtered.index[i], :]}')
        print(f'caminhao: {cam_ant.df_filtered.loc[13,["latitude","longitude","status","date_created"]].values}, dist: {round(great_circle(cam_ant.gps[13],esc_gps_fil_values[i]).m,2)}, escavadeira: {esc.df_filtered.loc[esc.df_filtered.index[i],["latitude","longitude","status","date_created"]].values}\n')
        

sys.exit()


fig = go.Figure(go.Scattermapbox(
    mode = "markers+lines",
    lon = cam_ant.gps[:,1],
    lat = cam_ant.gps[:,0],
    text = 'caminhao',
    marker = {'size': 10,
              'color': 'blue'}))
    

fig.add_trace(go.Scattermapbox(
    mode = "markers+lines",
    lon = esc.gps[:,1],
    lat = esc.gps[:,0],
    text = 'escavadeira',
    marker = {'size': 10,
              'color': 'red'}))

fig.update_layout(
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'center': {'lon': -38.71901, 'lat':  -3.94467},
        'style': "stamen-terrain",
        'center': {'lon': -38.71901, 'lat': -3.94467},
        'zoom': 15})

fig.show()


# np.savetxt('dados/gps_esc_datas.csv', gps, fmt='%.6f', delimiter=',')
# gps.to_csv('dados/gps_esc_datas.csv')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import sys
import platform as pl
from geopy.distance import great_circle

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
        self.df.columns = ["latitude", "longitude", "status", "angle", "fuel", "weight", "velocity", "imei", "date_created"]
        self.gps = self.df.loc[self.df['latitude'] < -1, ['latitude','longitude']].values
        self.df_filtered = self.df.loc[self.df['latitude'] < -1]
        self.gps_data = tuple(zip(self.df['latitude'].values, self.df['longitude'].values))

    def saveDataFrame(self, name_file):
        self.df_filtered.to_csv(name_file)



file_cam = 'logs_caminhao_18_08_21.csv'
file_esc = 'logs_escavadeira_18_08_21.csv'
cam = dataObject(file_cam)
esc = dataObject(file_esc)

esc_fil = esc.df_filtered.loc[esc.df_filtered['date_created'] > '2021-08-17 23:59:59']
esc_gps_fil = esc_fil.loc[:,['latitude','longitude']].values

for i in range(len(esc_gps_fil)):
    if great_circle(cam.gps[13],esc_gps_fil[i]).m < 5:
        print(f'coo_cam: {cam.gps[13]}, coo_esc: {esc_gps_fil[i]}, idx_esc: {i}, dist: {great_circle(cam.gps[13],esc_gps_fil[i]).m}')

sys.exit()


fig = go.Figure(go.Scattermapbox(
    mode = "markers+lines",
    lon = cam.gps[:,1],
    lat = cam.gps[:,0],
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
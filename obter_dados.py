import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import sys

# pesos = np.array([850,600,750,1050,1150,800])
# conchada = lambda x:x[np.random.choice(x.shape[0],1, replace=False)][0]

def conchada():
    pesos = np.array([850,600,750,1050,1150,800])
    return pesos[np.random.choice(pesos.shape[0],1, replace=False)][0]


file = 'logs_caminhao_18_08_21.csv'
df = pd.read_csv(f"dados/{file}", encoding='iso-8859-1')
df.columns = ["latitude", "longitude", "status", "angle", "fuel", "weight", "velocity", "imei", "date_created"]
gps = df.loc[df['latitude'] < -1, ['latitude','longitude']].values
# df_filtered = df.loc[df['latitude'] < -1, :]
# df_filtered.to_csv('logs_caminhao_18_08_21_filtered.csv')
# print(df_filtered)
# # sys.exit()
gps_data = tuple(zip(df['latitude'].values, df['longitude'].values))

file2 = 'logs_escavadeira_18_08_21.csv'
df2 = pd.read_csv(f"dados/{file2}", encoding='iso-8859-1')
df2.columns = ["latitude", "longitude", "status", "angle", "fuel", "weight", "velocity", "imei", "date_created"]
gps2 = df2.loc[df2['latitude'] < -1, ['latitude','longitude']].values
gps_data2 = tuple(zip(df2['latitude'].values, df2['longitude'].values))
print(gps)


# sys.exit()


fig = go.Figure(go.Scattermapbox(
    mode = "markers+lines",
    lon = gps[:,1],
    lat = gps[:,0],
    text = 'caminhao',
    marker = {'size': 10,
              'color': 'blue'}))
    

fig.add_trace(go.Scattermapbox(
    mode = "markers+lines",
    lon = gps2[:,1],
    lat = gps2[:,0],
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
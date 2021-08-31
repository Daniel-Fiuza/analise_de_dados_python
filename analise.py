import pandas as pd
import numpy as np
import os
import json
from pathlib import Path

# dir_of_files = "LOGScaminhao"
dir_of_files = "/home/administrador/Documentos/LOGS_ADC"

def convert_to_csv(dir_of_files):
    count_success = 0; count_files = 0
    pathList = Path(dir_of_files).glob('*.txt')
    CSVfile = f"dados\{dir_of_files}.csv"
    if os.path.exists(CSVfile):
            os.remove(CSVfile) 

    for file in pathList:   
        with open(CSVfile, mode='a') as csv_file:

            with open(f'{dir_of_files}\{file.name}', 'r', encoding='utf-8',
                    errors='ignore') as f:
                count_files += 1
                try:
                    msg = f.read()
                    #remove caracteres nulos
                    msg = msg.rstrip('\x00')
                    print(f"filename: {file.name}, msg: {msg}")
                    csv_file.write(msg+'\n')
                    count_success += 1
                    # if count_success == 10:
                    #     break
                except:
                    continue
    
    print(f"Total de arquivos: {count_files} \
            \nArquivos lidos com sucesso: {count_success} \
            \nArquivos que falharam: {count_files - count_success} \
            \nPercentual de sucesso: {round((count_success/count_files)*100, 2)}%")


def analise_datas():
    # file = "logs_caminhao_18_08_21.csv"
    file = "logs_escavadeira_18_08_21.csv"
    df = pd.read_csv(f"dados\{file}", encoding='utf-8')
    df.columns = ["latitude", "longitude", "status", "angle", "fuel", "weight", "velocity", "imei", "date_created"]
    # df.sort_index(axis=1, level=None, ascending=True)
    # print(df.describe())
    # print(df.dtypes)
    # print(df.info())
    df["date_created"] = pd.to_datetime(df["date_created"])
    df.sort_values(by="date_created", ascending=False, inplace=True)
    # print(df[df["date_created"] > "2021-08-17 00:00:00"])
    # print(df[df["weight"] > 0])
    print(pd.get_option('display.max_rows'))

def convert_csv_to_json():
    CSVfile = "logs_caminhao_filtrado.csv"
    JSONfile = f"{CSVfile[:-4]}.json"
    msg_label = ["latitude", "longitude", "status", "angle", "fuel", "weight", "velocity", "imei", "date_created"]
    msg_dict = {}; msg_list = []; msg_string = ''

    with open(JSONfile, 'w') as f:
        with open(CSVfile, 'r') as csv_file:
            # msg = str(csv_file.readlines()).rstrip('\n')
            for msg in csv_file.readlines():
                msg = msg.rstrip('\n')
                for i, m in enumerate(msg.split(",")):
                    if msg_label[i] == "latitude" or \
                       msg_label[i] == "longitude" or \
                       msg_label[i] == "angle" or \
                       msg_label[i] == "velocity":  
                        msg_dict[msg_label[i]] = float(m)
                    if msg_label[i] == "fuel" or msg_label[i] == "weight":
                        msg_dict[msg_label[i]] = int(m)
                    if msg_label[i] == "status" or msg_label[i] == "imei" or msg_label[i] == "date_created":
                        if msg_label[i] == "imei":
                            msg_dict[msg_label[i]] = 25    
                        else:
                            msg_dict[msg_label[i]] = m
                    
                msg_string = json.dumps(msg_dict)
                f.write(f"{msg_string},")
                # msg_list.append(msg_string)       
            
    # with open(JSONfile, 'w') as f:
    #     f.write(str(msg_list))
    print(f"Arquivo {JSONfile} criado com sucesso!")

if __name__ == "__main__": 
    convert_to_csv(dir_of_files)
    # analise_datas()
    # convert_csv_to_json()

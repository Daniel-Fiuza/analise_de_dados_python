import pandas as pd
import numpy as np
import os
import json
from pathlib import Path

# dir_of_files = "LOGScaminhao"
dir_of_files = "/home/administrador/Documentos/LOGS_01_09_21/LOGS_caminhao_01_09_21"

# Obtém arquivos dentro de um diretório e os converte em um arquivo csv 
def convertFromPathToCsv(dir_of_files):
    count_success = 0; count_files = 0
    pathList = Path(dir_of_files).glob('*.txt')
    # CSVfile = f"dados\{dir_of_files}.csv"
    CSVfile = f"dados_csv/{dir_of_files.split('/')[-1]}.csv"
    if os.path.exists(CSVfile):
            os.remove(CSVfile) 

    for file in pathList:   
        with open(CSVfile, mode='a') as csv_file:

            # with open(f'{dir_of_files}\{file.name}', 'r', encoding='utf-8',
            with open(f'{dir_of_files}/{file.name}', 'r', encoding='utf-8',
                    errors='ignore') as f:
                count_files += 1
                try:
                    msg = f.read()
                    msg = msg.rstrip('\x00')
                    lat = msg.split(',')[0]
                    try:
                        lat = float(lat)
                    #remove caracteres nulos
                        print(f"filename: {file.name}, msg: {msg}")
                        csv_file.write(msg+'\n')
                        count_success += 1
                    except:
                        continue
                    # if count_success == 10:
                    #     break
                except:
                    continue
    
    print(f"Total de arquivos: {count_files} \
            \nArquivos lidos com sucesso: {count_success} \
            \nArquivos que falharam: {count_files - count_success} \
            \nPercentual de sucesso: {round((count_success/count_files)*100, 2)}%")


def convertCsvToJson(CSVfile, JSONfile):
    # CSVfile = "logs_caminhao_filtrado.csv"
    # JSONfile = f"dados_json/{CSVfile[:-4]}.json"
    msg_label = ["latitude", "longitude", "status", "angle", "fuel", "weight", "velocity", "imei", "date_created"]
    msg_dict = {}; msg_list = []; msg_string = ''
    count_lines = 0

    with open(JSONfile, 'w') as f:
        f.write('[')
        with open(CSVfile, 'r') as csv_file:
            for msg in csv_file.readlines():
                count_lines += 1
                msg = msg.rstrip('\n')
                for i, data in enumerate(msg.split(",")):
                    msg_dict[msg_label[i]] = data
                #     if msg_label[i] == "latitude" or \
                #        msg_label[i] == "longitude" or \
                #        msg_label[i] == "angle" or \
                #        msg_label[i] == "velocity":  
                #         msg_dict[msg_label[i]] = float(data)
                #     if msg_label[i] == "fuel" or msg_label[i] == "weight":
                #         msg_dict[msg_label[i]] = int(data)
                #     if msg_label[i] == "status" or msg_label[i] == "imei" or msg_label[i] == "date_created":
                #         msg_dict[msg_label[i]] = data
                    
                msg_string = json.dumps(msg_dict)
                f.write(f"{msg_string},") 
            f.seek(f.tell() - 1, os.SEEK_SET) 
            f.write(']')

    print(f"Arquivo: {JSONfile} criado com sucesso!")


# Obtem os logs do diretorio, organiza pelo timestamp (constituído no nome de cada log) e gera o arquivo csv
def sort_files(dir_of_files):
    count_success = 0; count_files = 0
    pathList = Path(dir_of_files).glob('*.txt')
    CSVfile = f"dados/{dir_of_files.split('/')[-1]}.csv"
    if os.path.exists(CSVfile):
            os.remove(CSVfile) 

    for file in pathList:

        with open(CSVfile, mode='a') as csv_file:
            with open(f'{dir_of_files}/{file.name}', 'r', encoding='utf-8',
                        errors='ignore') as f:
                count_files += 1
                try:
                    datetime_list = file.name[:-4].split("_")
                    datetime_str = f"{datetime_list[0].zfill(2)}/{datetime_list[1].zfill(2)}/{datetime_list[2].zfill(2)} {datetime_list[3].zfill(2)}:{datetime_list[4].zfill(2)}:{datetime_list[5].zfill(2)}"
                    msg = f.read()
                    #remove caracteres nulos
                    msg = msg.rstrip('\x00')
                    print(f"filename: {file.name}, msg: {msg}")
                    if msg != "":
                        csv_file.write(msg+','+datetime_str+'\n')
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


def convert_csv_to_json_modified():
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

# Analisa arquivo de mensagens da serial do microcontrolador e o analisa 
def manage_files():
    filename = "/home/administrador/Documentos/TESTE_SDCARD/log_abdi.txt"
    count_success = 0
    count_fail = 0
    count_lora = 0
    count_problem = 0
    count_lines = 0
    with open(filename, 'r', encoding='utf-8') as f:
        msg = f.readline()
        msg = msg.rstrip('\x00')
        if "Escrito com sucesso no arquivo" in msg:
            count_success += 1
        if "Problema ao montar SDCard" in msg:
            count_fail += 1
        if "LoraBuffer:" in msg:
            count_lora += 1
        if "Erro ao escrever arquivo:" in msg:
            count_problem += 1
        count_lines += 1
        while msg != "":
            count_lines += 1
            msg = f.readline()
            msg = msg.rstrip('\x00')
            # count += 1
            if "Escrito com sucesso no arquivo" in msg:
                count_success += 1
            if "Problema ao montar SDCard" in msg:
                count_fail += 1
            if "LoraBuffer:" in msg:
                count_lora += 1
            if "Erro ao escrever arquivo:" in msg:
                count_problem += 1
            print(msg)
    print(f"Salvo {count_success} arquivos com sucesso \
            \nProblema ao montar SDCard: {count_fail} \
            \nQuantidade de LoraBuffer: {count_lora} \
            \nErro ao escrever arquivo: {count_problem} \
            \nTotal linhas do arquivo: {count_lines}")


# Verifica o arquivo de logs do sdcard e o arquivo de leitura da serial do microcontrolador, identificando possíveis arquivos faltantes.
def compare_files():
    pathname = "/home/administrador/Documentos/TESTE_SDCARD/log_abdi"
    filename = "/home/administrador/Documentos/TESTE_SDCARD/log_abdi.txt"
    pathList = Path(pathname).glob('*.txt')
    filesList = []
    errorFiles = []
    for files in pathList:
        filesList.append(files.name)

    with open(filename, 'r', encoding='utf-8') as f:
        msg = f.readline()
        msg = msg.rstrip('\x00')
        #eg: Escrito com sucesso no arquivo: LOGS/24_8_21_15_13_34.txt
        if "Escrito com sucesso no arquivo" in msg:
            filename = msg.split('/')[-1]
            filename = filename.rstrip('\n')
            if filename in filesList:
                ...
            else:
                errorFiles.append(filename)
        while msg != "":
            msg = f.readline()
            msg = msg.rstrip('\x00')
            if "Escrito com sucesso no arquivo" in msg:
                filename = msg.split('/')[-1]
                filename = filename.rstrip('\n')
                if filename in filesList:
                    ...
                else:
                    errorFiles.append(filename)
    print(f"Arquivos que deram erro: \
            {errorFiles} \
            \n\nQuantidade de arquivos: {len(errorFiles)}")
    # with open(f'{dir_of_files}/{file.name}', 'r', encoding='utf-8',
    #                     errors='ignore') as f:


if __name__ == "__main__": 
    CSVfile = "dados_csv/logs_abdi_2.csv"
    JSONfile = f"dados_json/{CSVfile[10:-4]}.json"
    PathFiles = "/home/usuario/Documentos/Docs/DadosColetadosTucunduba/escavadeira/logs_escavadeira_24_09"
    # convertCsvToJson(CSVfile,JSONfile)
    convertFromPathToCsv(PathFiles)

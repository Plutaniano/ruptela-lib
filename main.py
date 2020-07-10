import sys
import time
import os
os.system('cls')
print('Logando no Locator...')
from locator import *
time.sleep(2)
os.system('cls')

create_clients()
for client in Client.all:
    print(client)
CLIENT = Client.all[int(input('Selecione o cliente que deseja atribuir as modificações: '))] # sanitanizar input

for i, item in enumerate(hardwares):
    print(f'[ID:{i}] {item}')
id = int(input('Inserir ID do hardware desejado: '))
HARDWARE = list(hardwares.keys())[id]

def parse_phones():
    telephones = []
    while telephones == []:
        try:
            with open('telefones.txt') as f:
                lines = f.readlines()
                for line in lines:
                    telephones.append(line.replace('\n', ''))
        except FileNotFoundError:
            print('Não foi possível encontrar o arquivo telefones.txt ou ele está vazio')
            input('pressione qualquer tecla para tentar novamente.')
    return telephones

print('Lendo telefones...')
for n, telephone in enumerate(parse_phones()):
    print(f'\nTelefone: {telephone}')
    imei = input('Inserir IMEI: ')
    create_sim(telephone, CLIENT)
    # create_object(f'{CLIENT.company} [{imei[-6:]}]', imei, hardwares[HARDWARE], phone, CLIENT.id)
    print(f'{CLIENT.company} [{imei[-6:]}], imei:{imei}, hw:{HARDWARE}, telefone:{telephone}, id:{CLIENT.id}')

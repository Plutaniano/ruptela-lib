import sys
import time
import os
import atexit
import serial
from serial.tools.list_ports import comports

from arqia import Arqia
from classes import *
from cfg import *
from fw import *

def print_header():
    clear()
    print('      :::::::::::::    ::: :::::::: :::::::::::::       ::::::::: :::::::::') 
    print('     :+:       :+:    :+::+:    :+::+:       :+:       :+:    :+::+:    :+:') 
    print('    +:+        +:+  +:+ +:+       +:+       +:+       +:+    +:++:+    +:+ ') 
    print('   +#++:++#    +#++:+  +#+       +#++:++#  +#+       +#++:++#+ +#++:++#:   ') 
    print('  +#+        +#+  +#+ +#+       +#+       +#+       +#+    +#++#+    +#+   ') 
    print(' #+#       #+#    #+##+#    #+##+#       #+#       #+#    #+##+#    #+#    ') 
    print('#############    ### ######## ############################# ###    ###     ')
    try:
        print(f'Hardware: {HARDWARE.name}    Cliente: {CLIENT.company}')
    except:
        pass
    print('\n\n')


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def list_ruptela_devices():
    ruptela_devices = []
    for device in comports():
        if 'STMicroelectronics' in device.description:
            ruptela_devices.append(device)
    return ruptela_devices


if __name__ == '__main__':
    print_header()
    print('Cadastrador Ruptela v.02, utilizar somente com dispositivos Eco4 light+ S (3G ou não).\n')

    print('[ * ]\t Abrindo site da Arqia...')
    a = Arqia()
    if a.logged_in == True:
        print('--->\t Login OK!')

    print('[ * ]\t Logando no Locator...')
    l = Locator()
    if l.logged_in == True:
        print('--->\t Login OK!')

    print_header()
    CLIENT = Client.select_client()

    print_header()
    # força a escolha de FM-Eco4 S e renomeia para Eco4 light+ S
    # para evitar futuras confusões
    HARDWARE = Hardware.all[2]
    assert HARDWARE.name == 'FM-Eco4 S'
    HARDWARE.name = 'FM-Eco4 light+ S'

    while 1:

        ICCID = ''
        IMEI = ''
        SN = ''
        FW = ''
        CONFIG = ''
        phone = ''
        name = ''
        erro = ''

        while bool(ICCID and IMEI and SN and FW and CONFIG) == False:
            dispositivos = []
            while not FW:
                print_header()
                print(f'[ * ] Atualização de firmware')
                print('--->\t Buscando arquivo *.efwk4...')

                try:
                    fw_file = FW_File('')
                except FileNotFoundError as e:
                    print(f'[ERR] {e}')
                    print(f'---> Coloque um arquivo .efwk4 na pasta do programa e tente novamente.')
                    input('<---\t Pressione ENTER para tentar novamente.')
                    continue

                dispositivos = list_ruptela_devices()
                if len(dispositivos) > 1:
                    print('--->\t Mais de um dispositivo Ruptela detectado.')
                    input('--->\t Conecte somente um dispositivo e pressione ENTER para tentar novamente.')

                elif len(dispositivos) == 0:
                    print(f'---\t Por favor, conecte o dispositivo no computador via USB.')
                    input('--->\t Pressione ENTER para tentar novamente.')

                else:
                    port = dispositivos[0].device
                    print(f'--->\t Dispositivo detectado na porta \"{port}\", iniciando atualização de firmware.')
                    try:
                        FW = not fw_file.write(port)
                        print('--->\t Aguardando 15 segundos para reinicialização do dispositivo, por favor mantenha-o conectado.')
                        time.sleep(15)
                    except Exception as e:
                        print(f'[ERR] {e}')
                        input('<---\t Digite ENTER para tentar novamente.')
                    
            
            while not CONFIG:
                print_header()
                print(f'[ * ] Atualização de config')
                print('--->\t Buscando arquivo *.fk4c...')

                try:
                    config_file = Config_File()
                except FileNotFoundError as e:
                    print(f'[ERR]\t {e}')
                    print(f'--->\t Coloque um arquivo .fk4c na pasta do programa e tente novamente.')
                    input('<---\t Pressione ENTER para tentar novamente.')
                    continue

                dispositivos = list_ruptela_devices()
                if len(dispositivos) > 1:
                    print('--->\t Mais de um dispositivo Ruptela detectado.')
                    input('<---\t Conecte somente um dispositivo e pressione ENTER para tentar novamente.')

                elif len(dispositivos) == 0:
                    print(f'--->\t Por favor, conecte o dispositivo no computador via USB.')
                    input('<---\t Pressione ENTER para tentar novamente.')

                else:
                    port = dispositivos[0].device
                    print(f'--->\t Dispositivo detectado na porta \"{port}\", iniciando atualização de config.')
                    try:
                        CONFIG = not config_file.write(port)
                    except Exception as e:
                        print(f'[ERR] {e}')
                        input('<---\t Digite ENTER para tentar novamente.')



            print_header()
            print('Firmware:'.rjust(22, " ") + ' OK')
            print('Config:'.rjust(22, " ") + ' OK')
            print(f'{"ICCID:".rjust(22, " ")} {ICCID}')
            print(f'{"IMEI:".rjust(22, " ")} {IMEI}')
            print(f'Número de Série Excel: {SN}')
            print(f'\n{erro}')
            erro = ''
            reading = input('--->\t Esperando leitura do codigo de barras: ')

            try:
                int(reading)

            except ValueError:
                erro = 'valor nao-numérico inserido'

            finally:
                if len(reading) == 20:
                    try:
                        phone = a.find_by_ICCID(reading).phone
                        ICCID = reading
                    except KeyError as e:
                        erro = 'Não foi possível encontrar um sim card com o ICCID digitado.'

                elif len(reading) == 9:
                    SN = reading
                    name = f'{CLIENT.company} [{SN}]'
                
                elif len(reading) == 16:
                    IMEI = reading
                
                else:
                    erro = 'numero invalido'

        print_header()
        print('Firmware:'.rjust(22, " ") + ' OK')
        print('Config:'.rjust(22, " ") + ' OK')
        print(f'{"ICCID:".rjust(22, " ")} {ICCID}')
        print(f'{"IMEI:".rjust(22, " ")} {IMEI}')
        print(f'Número de Série Excel: {SN}')

        if input('\nDigite \'s\' para criar objeto ou qualquer outra tecla para descartar: ') in ['s', 'S']:

            print_header()            
            phone = a.find_by_ICCID(ICCID).phone
            l.create_new_object(name, IMEI, HARDWARE, phone, CLIENT, serial=SN)
            print('\n\n')

        print('O dispositivo já pode ser desconectado com segurança.')
        print('Pressione x para sair ou qualquer outra tecla para repetir: ')
        if input() in ['x', 'X']:
            quit()



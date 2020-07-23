import sys
import time
import os
import arqia
import atexit
from classes import Client, Web_User, Hardware, Packet, Object
from locator import *
from arqia import Arqia

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
    print('\n\n\n')


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')



if __name__ == '__main__':
    print_header()

    print('[*] Abrindo site da Arqia...')
    a = Arqia()

    print('[*] Logando no Locator...')
    l = Locator()

    print_header()
    CLIENT = Client.select_client()

    print_header()
    HARDWARE = Hardware.select_hardware()

    while 1:

        ICCID = ''
        IMEI = ''
        SN = ''
        name = ''
        erro = ''

        while bool(ICCID and IMEI and SN) == False:
            print_header()

            print(f'{"ICCID:".rjust(16, " ")} {ICCID}')
            print(f'{"IMEI:".rjust(16, " ")} {IMEI}')
            print(f'Numero de Serie: {SN}')
            print(f'\n{color(erro)}')
            erro = ''
            reading = input('\n Esperando leitura do codigo de barras: ')

            try:
                int(reading)
            except ValueError:
                erro = 'valor nao-numerico inserido'
            finally:
                if len(reading) == 20:
                    ICCID = reading

                elif len(reading) == 9:
                    SN = reading
                    name = f'{CLIENT.company} [{SN}]'
                
                elif len(reading) == 16:
                    IMEI = reading
                
                else:
                    erro = 'numero invalido'

        print_header()
        print(f'{"ICCID:".rjust(16, " ")} {ICCID}')
        print(f'{"IMEI:".rjust(16, " ")} {IMEI}')
        print(f'Numero de Serie: {SN}')

        if input('\nDigite \'s\' para criar objeto: ') in ['s', 'S']:
            sim_card = a.find_by_ICCID(ICCID)
            l.create_new_object(name, IMEI, HARDWARE, sim_card.phone, CLIENT, serial=SN)
            print('\n\n')

        print('Pressione x para sair ou qualquer outra tecla para repetir: ')
        if input() in ['x', 'X']:
            quit()



import sys
import time
import os
import arqia
from classes import Client, Web_User, Hardware, Packet, Object
from locator import Locator
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
        print(f'Hardware: {HARDWARE}    Cliente: {CLIENT.company}')
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
        print_header()
        ICCID = input('Escaneie o código de barras do SIM card: ')

        print_header()
        IMEI = input('Escaneie o IMEI do dispositivo: ')

        print_header()
        SN = input('Escaneie o Serial Number do dispositivo: ')


        name = f'{CLIENT.company} [{IMEI[-6:]}]'
        phone = a.find_by_ICCID(ICCID)


        create_object(name, IMEI, HARDWARE, phone, CLIENT.id, serial=SN)
        print('\n\n')

        print('Pressione x para sair ou qualquer outra tecla para repetir: ')
        if input() in ['x', 'X']:
            quit()


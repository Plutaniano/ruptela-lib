import sys
import time
import os
import arqia
from locator import Locator

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


def select_client(locator):
    for client in locator.clients:
        print(f'[{client.index}] {client.company}')
    print('\n\n')
    index = int(input('Selecione o cliente que deseja atribuir as modificações: '))
    return locator.clients[index]





if __name__ == '__main__':
    print_header()

    print('[*] Abrindo site da Arqia...')
    arqia.login(arqia.options())

    print('[*] Logando no Locator...')
    l = Locator()

    print_header()
    CLIENT = select_client(l)

    print_header()
    HARDWARE = select_hardware(l)

    while 1:
        print_header()
        ICCID = input('Escaneie o código de barras do SIM card: ')

        print_header()
        IMEI = input('Escaneie o IMEI do dispositivo: ')

        print_header()
        SN = input('Escaneie o Serial Number do dispositivo: ')


        name = f'{CLIENT.company} [{IMEI[-6:]}]'
        phone = ICCID_to_phone(ICCID)


        create_object(name, IMEI, HARDWARE, phone, CLIENT.id, serial=SN)
        print('\n\n')

        print('Pressione x para sair ou qualquer outra tecla para repetir: ')
        if input() in ['x', 'X']:
            quit()


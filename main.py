import sys
import time
import os

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
    from arqia import *

    print('[*] Logando no Locator...')
    from locator import *

    print('[*] Obtendo clientes...',)
    create_clients()
    time.sleep(1)

    print_header()
    CLIENT = select_client()

    print_header()
    HARDWARE = select_hardware()

    while 1:
        print_header()
        ICCID = input('Escaneie o código de barras do SIM card: ')

        print_header()
        IMEI = input('Escaneie o IMEI do dispositivo: ')


        name = f'{CLIENT.company} [{IMEI[-6:]}]'
        phone = ICCID_to_phone(ICCID)


        create_sim(phone, CLIENT.id)
        print('\n\n')
        create_object(name, IMEI, HARDWARE, phone, CLIENT.id)
        print('\n\n')

        print('Pressione x para sair ou qualquer outra tecla para repetir: ')
        if input() in ['x', 'X']:
            quit()


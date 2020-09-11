import smtplib, ssl


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

def err_str(msg):
    return f'{colored.back.RED}{msg}{colored.style.RESET}'

def ok_str(msg):
    return f'{colored.back.GREEN}{msg}{colored.style.RESET}'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def send_email(message, subject='', to='lucas.rodrigues@excelbr.com.br'):
    port = 465
    sender_user = 'excel.ruptela.info@gmail.com'
    sender_password = 'excelbr123$'

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(sender_user, sender_password)
        server.sendmail(sender_user, to, 'test')

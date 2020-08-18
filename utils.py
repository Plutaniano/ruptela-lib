import smtplib, ssl


def send_email(message, subject='', to='lucas.rodrigues@excelbr.com.br'):
    port = 465
    sender_user = 'excel.ruptela.info@gmail.com'
    sender_password = 'excelbr123$'

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(sender_user, sender_password)
        server.sendmail(sender_user, to, 'test')

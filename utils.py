import smtplib, ssl

port = 465
sender_user = 'excel.ruptela.info@gmail.com'
sender_password = 'excelbr123$'
target_email = 'lucas.rodrigues@excelbr.com.br'

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
    server.login(sender_user, sender_password)
    server.sendmail(sender_user, target_email, 'test')
        
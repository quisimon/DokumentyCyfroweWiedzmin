import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from smtpd import SMTPServer
from datetime import datetime

SMTP_PORT = 2137
EMAIL_ADDRESS = 'kan.red.bes@gmail.com'
BODY = 'W zalaczniku umieszczamy szczegoly Panskiego zlecenia wiedzminskiego.\n\n' \
       'Z wyrazami szacunku\n' \
       'Kancelaria Redukcji Bestii'


def start_smtp_server():
    server = SMTPServer(('localhost', SMTP_PORT), None)
    print(f'Starting SMTP server on port {SMTP_PORT}...')
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.close()


def send_email(recipient_email, xml_file_path, pdf_file_path):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    msg['Subject'] = 'Zlecenie wiedzminskie ' + datetime.now().strftime('%d.%m.%Y')

    msg.attach(MIMEText(BODY, 'plain'))
    attach_file(msg, xml_file_path)
    attach_file(msg, pdf_file_path)

    with smtplib.SMTP('localhost', SMTP_PORT) as server:
        server.send_message(msg)

    print(f'Email sent successfully to {recipient_email}.')


def attach_file(msg, file_path):
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
        msg.attach(part)

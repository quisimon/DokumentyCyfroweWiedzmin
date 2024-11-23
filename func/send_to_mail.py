import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'kan.red.bes@gmail.com'
EMAIL_PASSWORD = 'zaq1@WSX'
BODY = 'W załączniku umieszczamy szczegóły Waszego zlecenia wiedźminskiego.\n\n' \
       'Z wyrazami szacunku\n' \
       'Kancelaria Redukcji Bestii'


def send_email(recipient_email, xml_file_path, pdf_file_path):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    msg['Subject'] = 'Zlecenie wiedźminskie ' + datetime.now().strftime('%d.%m.%Y')

    msg.attach(MIMEText(BODY, 'plain'))
    attach_file(msg, xml_file_path)
    attach_file(msg, pdf_file_path)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

    print(f'Email sent successfully to {recipient_email}.')


def attach_file(msg, file_path):
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
        msg.attach(part)

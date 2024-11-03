from threading import Thread

from func.google_drive import upload_file
import func.send_to_mail


if __name__ == '__main__':
    # Start up an SMTP server for sending out the mails
    # server_thread = Thread(target=func.send_to_mail.start_smtp_server)
    # server_thread.start()
    pass
    # upload_file('example.json', 'example.json')
    # upload_file('example.pdf', 'example.pdf')
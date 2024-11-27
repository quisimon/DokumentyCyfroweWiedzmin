from threading import Thread
import os
from func.google_drive import upload_file
import func.google_drive
import func.gotowy_generator_html
import func.gotowy_generator_html.xml_to_html_updated
import func.send_to_mail
import func.pdf_reader
from func.xml_to_pdf import generate_pdf_with_json_data
from func.form_data_to_json import save_form_data_to_json
import flask
from flask import send_from_directory
import func.camunda as camunda
import time
import requests
import json

import func.xml_to_html


task_1_id = -1
task_2_id = -1


# INIT CAMUNDA
url = "https://login.cloud.camunda.io/oauth/token"  
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}
data = {
    'grant_type': 'client_credentials',
    'audience': "tasklist.camunda.io",  
    'client_id': "41skPyw0WaCjc2TC5YldukfWZTTcZOPy",      
    'client_secret': "w7250f5koPZSBQQ5VMciCmbKsE71MUFUlDinlueGt1vliXWVNKj1sIzTFVmfTfHu"  
}

response = requests.post(url, headers=headers, data=data)

print("\n\nAccess token request response: ", response.status_code)

access_token = response.json().get("access_token")
print("Access token has been saved")

from pyzeebe import ZeebeClient, create_camunda_cloud_channel, ZeebeWorker
import asyncio

channel = create_camunda_cloud_channel("41skPyw0WaCjc2TC5YldukfWZTTcZOPy", "w7250f5koPZSBQQ5VMciCmbKsE71MUFUlDinlueGt1vliXWVNKj1sIzTFVmfTfHu", "eea87386-0393-4bbc-ad2e-a10a85bb2646")
client = ZeebeClient(channel)
worker = ZeebeWorker(channel)

async def create_instance():
    global process_instance_key
    process_instance_key = await client.run_process("Process_1r7tjf2") 

loop = asyncio.get_event_loop()
loop.run_until_complete(create_instance())
print("Created process instance: ", process_instance_key.process_instance_key)
# END CAMUNDA INIT

app = flask.Flask(__name__)
app.secret_key = 'KanRedBes'
form_data = []
sections_count = 0

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    global form_data
    flask.session['next_section'] = 1
    form_data = []
    return flask.render_template('index.html')


# Route to handle file upload and processing
@app.route('/upload', methods=['POST'])
def upload_file():
    global form_data, sections_count, task_1_id
    if 'file' not in flask.request.files:
        return 'Nie wybrano pliku!', 400
    file = flask.request.files['file']
    if file.filename == '':
        return 'Nie wybrano pliku!', 400

    flask.session['next_section'] = 1
    form_data = []
    pdf_template_filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(pdf_template_filepath)

    func.pdf_reader.read_pdf(pdf_template_filepath)
    sections_count = func.xml_to_html.generate_htmls_from_xml('output.xml')

    task_1_id = camunda.get_task_1(access_token, process_instance_key)

    return flask.redirect(flask.url_for('handle_section', step=flask.session['next_section']))
    

@app.route('/form/section/<int:step>', methods=['GET', 'POST'])
def handle_section(step):
    global form_data, sections_count, task_2_id
    if flask.request.method == 'GET':
        if step == 2 and form_data[0]['Miejsce zamieszkania (wybrać jedno)'] == 'Wieś':
            flask.session['next_section'] = step + 1
            camunda.complete_task_1(access_token, task_1_id, 0)
            task_2_id = camunda.get_task_2(access_token, process_instance_key)
            return flask.redirect(flask.url_for('handle_section', step=flask.session['next_section'])) 
            
        if step == 3 and form_data[0]['Miejsce zamieszkania (wybrać jedno)'] == 'Miasto':
            flask.session['next_section'] = step + 1
            camunda.complete_task_1(access_token, task_1_id, 1)
            task_2_id = camunda.get_task_2(access_token, process_instance_key)
            return flask.redirect(flask.url_for('handle_section', step=flask.session['next_section'])) 

        if step == 6 and form_data[3]['Czy zidentyfikowano potwora (wybrać jedno)'] == 'Nie':
            flask.session['next_section'] = step + 1
            camunda.complete_task_2(access_token, task_1_id, 0)
            return flask.redirect(flask.url_for('handle_section', step=flask.session['next_section'])) 
        
        if step == 7 and form_data[3]['Czy zidentyfikowano potwora (wybrać jedno)'] == 'Tak':
            flask.session['next_section'] = step + 1
            camunda.complete_task_2(access_token, task_1_id, 1)
            return flask.redirect(flask.url_for('handle_section', step=flask.session['next_section'])) 

        return flask.render_template(f"section_{step}.html")
    
    form_data.append(flask.request.form.to_dict())
    flask.session['next_section'] = step + 1
    if flask.session['next_section'] > sections_count:
        return flask.redirect(flask.url_for('summary'))
    
    return flask.redirect(flask.url_for('handle_section', step=flask.session['next_section'])) 


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/summary', methods = ['GET', 'POST'])
def summary():
    global form_data
    if flask.request.method == 'POST':
        func.send_to_mail.send_email(flask.request.form['recipient_email'], 'output.xml', 'uploads/output.pdf')

    else:
        save_form_data_to_json(form_data, 'uploads/form_data.json')
        generate_pdf_with_json_data('output.xml', form_data, 'uploads/output.pdf')
        func.google_drive.upload_file('uploads/output.pdf', f"Formularz_{form_data[0]['Imię']}_{form_data[0]['Nazwisko']}.pdf", 'formularze')

    return flask.render_template('summary.html', pdf_url=flask.url_for('uploaded_file', filename='output.pdf'))

app.run()

#upload_file('example.json', 'example.json')
#upload_file('example.pdf', 'example.pdf')

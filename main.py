from threading import Thread
import os
from func.google_drive import upload_file
import func.gotowy_generator_html
import func.gotowy_generator_html.xml_to_html_updated
import func.send_to_mail
import func.pdf_reader
import flask

import func.xml_to_html


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
    global form_data, sections_count
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

    return flask.redirect(flask.url_for('handle_section', step=flask.session['next_section']))
    

@app.route('/form/section/<int:step>', methods=['GET', 'POST'])
def handle_section(step):
    global form_data, sections_count
    if flask.request.method == 'GET':
        if step == 2 and form_data[0]['Miejsce zamieszkania (wybrać jedno)'] == 'Wieś':
            flask.session['next_section'] = step + 1
            return flask.redirect(flask.url_for('handle_section', step=flask.session['next_section'])) 
            
        if step == 3 and form_data[0]['Miejsce zamieszkania (wybrać jedno)'] == 'Miasto':
            flask.session['next_section'] = step + 1
            return flask.redirect(flask.url_for('handle_section', step=flask.session['next_section'])) 

        if step == 6 and form_data[3]['Czy zidentyfikowano potwora (wybrać jedno)'] == 'Nie':
            flask.session['next_section'] = step + 1
            return flask.redirect(flask.url_for('handle_section', step=flask.session['next_section'])) 
        
        if step == 7 and form_data[3]['Czy zidentyfikowano potwora (wybrać jedno)'] == 'Tak':
            flask.session['next_section'] = step + 1
            return flask.redirect(flask.url_for('handle_section', step=flask.session['next_section'])) 

        return flask.render_template(f"section_{step}.html")
    
    form_data.append(flask.request.form.to_dict())
    flask.session['next_section'] = step + 1
    if flask.session['next_section'] > sections_count:
        return flask.redirect(flask.url_for('summary'))
    
    return flask.redirect(flask.url_for('handle_section', step=flask.session['next_section'])) 


@app.route('/summary')
def summary():
    global form_data
    print(form_data)

app.run()

# upload_file('example.json', 'example.json')
# upload_file('example.pdf', 'example.pdf')

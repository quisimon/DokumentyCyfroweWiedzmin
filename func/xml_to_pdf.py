import xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import json

def get_dynamic_sections(xml_filepath, form_data):
    tree = ET.parse(xml_filepath)
    root = tree.getroot()

    selected_sections = []
    for section in root.findall("./section"):
        section_id = section.get("section_id")
        section_name = section.get("section_name")
        include_section = True

        if section_id == "2A" and form_data[0].get("Miejsce zamieszkania (wybrać jedno)") != "Miasto":
            include_section = False
        elif section_id == "2B" and form_data[0].get("Miejsce zamieszkania (wybrać jedno)") != "Wieś":
            include_section = False
        elif section_id == "5A" and form_data[3].get("Czy zidentyfikowano potwora (wybrać jedno)") != "Tak":
            include_section = False
        elif section_id == "5B" and form_data[3].get("Czy zidentyfikowano potwora (wybrać jedno)") != "Nie":
            include_section = False

        if include_section:
            fields = []
            for field in section:
                if field.tag in ["input_field", "radio_button", "list"]:
                    fields.append({
                        "field_name": field.get("field_name") or field.get("name"),
                        "required": field.get("required") == "true",
                        "type": field.tag,
                        "options": [option.get("option_name") for option in field.findall("./option")],
                    })
            selected_sections.append({
                "section_id": section_id,
                "section_name": section_name,
                "fields": fields,
            })

    return selected_sections

def fill_sections_with_data(selected_sections, form_data):
    filled_sections = []
    for section in selected_sections:
        filled_fields = []
        for field in section["fields"]:
            field_name = field["field_name"]
            field_value = "N/A"
            for entry in form_data:
                if field_name in entry:
                    field_value = entry.get(field_name, "N/A")
                    break
            filled_fields.append({
                "field_name": field_name,
                "value": field_value,
                "type": field["type"],
            })
        filled_sections.append({
            "section_name": section["section_name"],
            "fields": filled_fields,
        })
    return filled_sections

def generate_pdf_with_json_data(xml_filepath, form_data, output_filepath):
    tree = ET.parse(xml_filepath)
    root = tree.getroot()

    #with open('../form_data.json', "r", encoding="utf-8") as json_file:
    #    form_data = json.load(json_file)

    selected_sections = get_dynamic_sections(xml_filepath, form_data)

    filled_sections = fill_sections_with_data(selected_sections, form_data)

    c = canvas.Canvas(output_filepath)

    pdfmetrics.registerFont(TTFont('Arial', '../Fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', '../Fonts/arialbd.ttf'))

    c.setFont("Arial-Bold", 20)
    c.drawCentredString(300, 800, "UMOWA O ZLECENIE WIEDŹMIŃSKIE")

    y_position = 750
    for section in filled_sections:
        c.setFont("Arial-Bold", 14)
        c.drawString(50, y_position, section["section_name"])
        y_position -= 20

        for field in section["fields"]:
            c.setFont("Arial", 12)
            field_text = f"{field['field_name']}: {field['value']}"
            c.drawString(50, y_position, field_text)
            y_position -= 15

        y_position -= 10
        if y_position < 50:
            c.showPage()
            y_position = 800

    c.save()

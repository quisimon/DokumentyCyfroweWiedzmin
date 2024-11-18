import re
import xml.etree.ElementTree as ET

from pdfminer.high_level import extract_text

def read_pdf(file_name):
    text = extract_text(file_name).split("\n")
    text: list[str] = list(filter(lambda x: x != "" and x != ' ', text))
    text = [re.sub(r"^\x0c+", "", item) for item in text]

    root = ET.Element("form")
    current_section = None
    current_subelement = None
    current_subelement_type = None

    for phrase in text[1:len(text) - 1]:
        if "." in phrase.strip():
            section_id = phrase.split(". ")[0]
            section_name = phrase.split(". ")[1]
            section = ET.SubElement(root, "section", section_id=section_id, section_name=section_name)
            current_section = section
        elif "(wybrać jedno)" in phrase.strip():
            if "*" in phrase.strip():
                button_name = phrase.replace("*:", "")
                required = "true"
            else:
                button_name = phrase.replace(":", "")
                required = "false"
            button = ET.SubElement(current_section, "radio_button", name=button_name, required=required)
            current_subelement = button
            current_subelement_type = "radio_button"
        elif "(wybrać z listy)" in phrase.strip():
            if "*" in phrase.strip():
                button_name = phrase.replace("*:", "")
                required = "true"
            else:
                button_name = phrase.replace(":", "")
                required = "false"
            button = ET.SubElement(current_section, "list", name=button_name, required=required)
            current_subelement = button
            current_subelement_type = "list"
        elif phrase.strip()[0] == "–":
            if current_subelement_type == "list":
                ET.SubElement(current_subelement, "list_option", name=phrase.replace("– ", ""))
            else:
                ET.SubElement(current_subelement, "option", option_name=phrase.replace("– ", ""))
        else:
            if "*" in phrase.strip():
                ET.SubElement(current_section, "input_field", field_name=phrase.replace("*:", ""), required="true")
            else:
                ET.SubElement(current_section, "input_field", field_name=phrase.replace(":", ""), required="false")
                
    tree = ET.ElementTree(root)
    ET.indent(tree, space="\t", level=0)
    tree.write("output.xml", encoding='utf-8', xml_declaration=True)



import xml.etree.ElementTree as ET


def generate_html_sections(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    sections = []

    for section in root.findall('section'):
        section_id = section.attrib.get("section_id", "")
        section_name = section.attrib.get("section_name", "")

        # HTML stylesheet link
        html = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "<meta charset='utf-8'>",
            "<link rel='stylesheet' type='text/css' href='../../static/styles.css'>",
            f"<title>{section_name}</title>",
            "</head>",
            "<body>",
            f"<div id='section_{section_id}' class='section'>",
            f"<h2>{section_name}</h2>",
            '<form method="post" enctype="multipart/form-data">'
        ]

        for element in section:
            if element.tag == "input_field":
                field_name = element.attrib.get("field_name", "")
                required = element.attrib.get("required", "false") == "true"

                label = f"<label>{field_name}{'*' if required else ''}:</label>"
                input_field = f"<input type='text' name='{field_name}' {'required' if required else ''}>"

                html.append(f"<div class='form-group'>{label}{input_field}</div>")

            elif element.tag == "radio_button":
                name = element.attrib.get("name", "")
                required = element.attrib.get("required", "false") == "true"

                html.append(f"<fieldset class='form-group'><legend>{name}{'*' if required else ''}:</legend>")

                for option in element:
                    option_name = option.attrib.get("option_name", "")
                    radio_input = f"<input type='radio' name='{name}' value='{option_name}' {'required' if required else ''}> {option_name}"
                    html.append(f"<div>{radio_input}</div>")

                html.append("</fieldset>")

            elif element.tag == "list":
                name = element.attrib.get("name", "")
                required = element.attrib.get("required", "false") == "true"

                html.append(f"<label>{name}{'*' if required else ''}:</label>")
                html.append(f"<select name='{name}' {'required' if required else ''}>")

                for list_option in element:
                    option_name = list_option.attrib.get("name", "")
                    html.append(f"<option value='{option_name}'>{option_name}</option>")

                html.append("</select>")

        html.append("<button type='submit'>Wyślij</button>")
        html.append("</form>")
        html.append("</div>")
        html.append("</body>")
        html.append("</html>")

        sections.append("\n".join(html))

    return sections


# Generate sections
def generate_htmls_from_xml(xml_filename):
    sections_html = generate_html_sections(xml_filename)
    for i, section_html in enumerate(sections_html, 1):
        with open(f"templates/section_{i}.html", "w", encoding="utf-8") as f:
            f.write(section_html)

    return len(sections_html)

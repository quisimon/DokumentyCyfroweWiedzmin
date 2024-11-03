import xml.etree.ElementTree as ET


def generate_html_form(xml_file, output_html_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    html = ["<!DOCTYPE html>", "<html lang='pl'>", "<head>",
            "<meta charset='UTF-8'>", "<title>UMOWA O ZLECENIE WIEDŹMIŃSKIE</title>",
            "<style>", "label { display: block; margin: 5px 0; }",
            "input[type='text'], select { width: 100%; padding: 8px; margin: 5px 0; }",
            "</style>", "</head>", "<body>", "<h1>UMOWA O ZLECENIE WIEDŹMIŃSKIE</h1>", "<form>"]

    def process_element(element):
        tag_name = element.tag.replace('_', ' ').capitalize()

        if element.attrib.get("required") == "true":
            label = f"<label>{tag_name}*:</label>"
        else:
            label = f"<label>{tag_name}:</label>"

        if len(element) > 0:
            if element.tag == "płeć":
                html.append(f"{label}")
                for sub in element:
                    html.append(f"<input type='radio' name='{element.tag}' value='{sub.tag}'> {sub.tag.capitalize()}")
            elif element.tag == "kwota_zlecenia":
                html.append(f"{label}")
                html.append("<input type='text' name='waluta' placeholder='Waluta'>")
                html.append("<input type='text' name='kwota' placeholder='Kwota'>")
            else:
                html.append(f"{label}")
                for sub in element:
                    process_element(sub)
        else:
            html.append(f"{label}<input type='text' name='{element.tag}'>")

    for child in root:
        process_element(child)

    html.extend(["<button type='submit'>Wyślij</button>", "</form>", "</body>", "</html>"])

    with open(output_html_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(html))

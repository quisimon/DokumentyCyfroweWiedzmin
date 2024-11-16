import xml.etree.ElementTree as ET

def generate_html_form(xml_file, output_html_file):
    # Define the list of monster types
    monster_types = ["Wilkołak", "Wampir", "Strzyga", "Leszy", "Kikimora", "Niezidentyfikowany"]

    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Begin the HTML form
    html = [
        "<!DOCTYPE html>",
        "<html lang='pl'>",
        "<head>",
        "<meta charset='UTF-8'>",
        "<meta name='viewport' content='width=device-width, initial-scale=1.0'>",
        "<title>UMOWA O ZLECENIE WIEDŹMIŃSKIE</title>",
        "<style>",
        "label { display: block; margin: 5px 0; }",
        "input[type='text'], select, textarea { width: 100%; padding: 8px; margin: 5px 0; }",
        ".radio-group { display: flex; gap: 10px; margin: 10px 0; }",
        "#cityData, #villageData, #monsterDescription { display: none; }",  # Initially hide sections
        "</style>",
        "</head>",
        "<body>",
        "<form id='contractForm'>",
        "<h1>UMOWA O ZLECENIE WIEDŹMIŃSKIE</h1>"
    ]

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
            if element.tag == "gatunek_potwora":
                # Add dropdown for monster types
                html.append(label)
                html.append(f"<select id='monsterType' name='{element.tag}'>")
                for monster in monster_types:
                    html.append(f"<option value='{monster}'>{monster}</option>")
                html.append("</select>")
                # Add description input, initially hidden
                html.append("<div id='monsterDescription'>")
                html.append("<label>Opis potwora:</label><textarea name='opis_potwora'></textarea>")
                html.append("</div>")
            else:
                html.append(f"{label}")
                for sub in element:
                    process_element(sub)
        else:
            html.append(f"{label}<input type='text' name='{element.tag}'>")

    for child in root:
        if child.tag == "dane_zlecającego":
            html.append("<h3>Dane zlecającego</h3>")
            for sub in child:
                if sub.tag == "miasto":
                    html.append("<label><input type='radio' name='residence' value='Miasto'> Miasto</label>")
                elif sub.tag == "wieś":
                    html.append("<label><input type='radio' name='residence' value='Wieś'> Wieś</label>")
                else:
                    process_element(sub)
        elif child.tag == "dane_zlecającego_miasto":
            html.append("<div id='cityData'>")
            html.append("<h3>Dane zlecającego miasto</h3>")
            for sub in child:
                process_element(sub)
            html.append("</div>")
        elif child.tag == "dane_zlecającego_wieś":
            html.append("<div id='villageData'>")
            html.append("<h3>Dane zlecającego wieś</h3>")
            for sub in child:
                process_element(sub)
            html.append("</div>")
        else:
            process_element(child)

    html.extend([
        "<button type='button' id='submitBtn'>Zapisz</button>",
        "</form>",
        "<script>",
        "// Show/hide fields based on residence choice",
        "document.querySelectorAll('input[name=\"residence\"]').forEach(radio => {",
        "    radio.addEventListener('change', function() {",
        "        document.getElementById('cityData').style.display = this.value === 'Miasto' ? 'block' : 'none';",
        "        document.getElementById('villageData').style.display = this.value === 'Wieś' ? 'block' : 'none';",
        "    });",
        "});",
        "// Show/hide monster description based on monster type",
        "document.addEventListener('DOMContentLoaded', function() {",
        "    const monsterTypeDropdown = document.getElementById('monsterType');",
        "    const monsterDescriptionDiv = document.getElementById('monsterDescription');",
        "    monsterTypeDropdown.addEventListener('change', function() {",
        "        if (this.value === 'Niezidentyfikowany') {",
        "            monsterDescriptionDiv.style.display = 'block';",
        "        } else {",
        "            monsterDescriptionDiv.style.display = 'none';",
        "        }",
        "    });",
        "});",
        "// Function to gather form data and convert to JSON",
        "function gatherFormData() {",
        "    const formData = {",
        "        dateAndPlace: document.querySelector('input[name=\"data_i_miejscowość\"]').value,",
        "        client: {",
        "            firstName: document.querySelector('input[name=\"imię\"]').value,",
        "            lastName: document.querySelector('input[name=\"nazwisko\"]').value,",
        "            gender: document.querySelector('input[name=\"płeć\"]:checked')?.value,",
        "            residence: document.querySelector('input[name=\"residence\"]:checked')?.value",
        "        },",
        "        monster: {",
        "            type: document.getElementById('monsterType').value,",
        "            description: document.querySelector('textarea[name=\"opis_potwora\"]')?.value || null",
        "        }",
        "    };",
        "    return JSON.stringify(formData, null, 2);",
        "}",
        "document.getElementById('submitBtn').addEventListener('click', function() {",
        "    const formDataJson = gatherFormData();",
        "    console.log(formDataJson);",
        "    alert('Formularz został zapisany!');",
        "});",
        "</script>",
        "</body>",
        "</html>"
    ])

    # Write the generated HTML to the output file
    with open(output_html_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(html))

# Call the function to generate the form
generate_html_form('output.xml', 'form.html')

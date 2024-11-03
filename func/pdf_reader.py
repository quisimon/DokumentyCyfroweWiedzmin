import re
import xml.etree.ElementTree as ET

from pdfminer.high_level import extract_text

def read_pdf(file_name):
    text = extract_text(file_name).split("\n")
    text: list[str] = list(filter(lambda x: x != "" and x != ' ', text))
    text = [re.sub(r"^\x0c+", "", item) for item in text]
    root = ET.Element("umowa_o_zlecenie")
    current_sub = root
    for phrase in text[1:len(text) - 1]:
        if phrase.strip().endswith("*:"):
            new_phrase = phrase.strip().lower().replace(" (wybrać jedno)", "").replace("*:", "").replace(" ", "_")
            if new_phrase.endswith("(ulica,_mieszkanie)"):
                np = "adres"
                element = ET.SubElement(current_sub, np)
                street = ET.SubElement(element, "ulica")
                local = ET.SubElement(element, "mieszkanie")
                street.text = " "
                local.text = " "
                continue
            elif new_phrase.endswith("płeć"):
                np = "płeć"
                element = ET.SubElement(current_sub, np, required="true")
                man = ET.SubElement(element, "mężczyzna")
                woman = ET.SubElement(element, "kobieta")
                other = ET.SubElement(element, "inna")
                man.text = " "
                woman.text = " "
                other.text = " "
                continue
            elif new_phrase.endswith("(w_orenach,_florenach_bądź_innej_walucie)"):
                np = "kwota_zlecenia"
                element = ET.SubElement(current_sub, np, required="true")
                waluta = ET.SubElement(element, "waluta")
                kwota = ET.SubElement(element, "kwota")
                waluta.text = " "
                kwota.text = " "
                continue
            elif new_phrase.endswith("(jeśli_zidentyfikowano)"):
                np = "gatunek_potwora"
                element = ET.SubElement(current_sub, np, identified="true")
                element.text = " "
                continue
            elif new_phrase.endswith("(jeśli_nie_zidentyfikowano)"):
                np = "opis_potwora"
                element = ET.SubElement(current_sub, np, identified="false")
                element.text = " "
                continue
            element = ET.SubElement(current_sub, new_phrase, required="true")
            element.text = " "
        elif phrase.strip()[0].isdigit():
            np = re.sub(r"^\w+\.\s*", "", phrase).strip().lower().replace(" (wybrać jedno)", "").replace("*:",
                                                                                                         "").replace(
                " ", "_")
            if np.endswith("(miasto)"):
                np = "dane_zlecającego_miasto"
            elif np.endswith("(wieś)"):
                np = "dane_zlecającego_wieś"
            element = ET.SubElement(root, np)
            element.text = " "
            current_sub = element
        elif phrase.strip() == "* pola obowiązkowe":
            continue
        elif phrase.strip() == "Strona 1 z 2":
            continue
        elif phrase.strip() == "Strona 2 z 2":
            continue
        elif phrase.strip() == "mężczyzna" or phrase.strip() == "kobieta" or phrase.strip() == "inna":
            continue
        elif phrase.strip().startswith("Zaliczka"):
            np = "zaliczka"
            element = ET.SubElement(current_sub, np)
            element.text = " "
            continue
        else:
            new_phrase = phrase.strip().lower().replace(" (wybrać jedno)", "").replace(":", "").replace(" ", "_")
            element = ET.SubElement(current_sub, new_phrase)
            element.text = " "

    tree = ET.ElementTree(root)
    tree.write("output.xml", encoding='utf-8', xml_declaration=True)

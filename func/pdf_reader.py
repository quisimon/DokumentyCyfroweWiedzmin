from pdfminer.high_level import extract_text


def read_pdf(file_name):
    text = extract_text(file_name).split("\n")
    text: list[str] = list(filter(lambda x: x != "", text))
    result = {}

    first = text.index("1. Dane zlecającego")
    second = text.index("2A. Dane zlecającego – ciąg dalszy (miasto)")
    third = text.index("2B. Dane zlecającego – ciąg dalszy (wieś)")
    fourth = text.index("3. Dane wiedźmina")
    fifth = text.index("4. Szczegóły zlecenia")

    date_and_place = get_date_and_place(text[1])
    orderer_data = get_orderer_data(text[first:second])
    city_data = get_city_data(text[second:third])
    village_data = get_village_data(text[third:fourth])
    witcher_data = get_witcher_data(text[fourth:fifth])
    details_data = get_details_data(text[fifth:])

    result["date and place"] = date_and_place
    result["orderer"] = orderer_data
    result["city"] = city_data
    result["village"] = village_data
    result["witcher"] = witcher_data
    result["details"] = details_data

    return result


def get_date_and_place(date_and_place: str):
    date_and_place_section = {}
    splitted = date_and_place.split(":")[1].strip().split(",")
    date_and_place_section["date"] = splitted[0].strip()
    date_and_place_section["place"] = splitted[1].strip()
    return date_and_place_section


def get_orderer_data(orderer_section: list[str]):
    orderer_data = {}
    for token in orderer_section:
        token = token.lower()
        if token.startswith("data i miejscowość"):
            splitted = token.split(":")[1].strip().split(",")
            orderer_data["date"] = splitted[0].strip()
            orderer_data["place"] = splitted[1].strip()
        elif token.startswith("imię"):
            orderer_data["name"] = token.split(":")[1].strip()
        elif token.startswith("nazwisko"):
            orderer_data["surname"] = token.split(":")[1].strip()
        elif token.startswith("płeć"):  # todo zapytac MG jak pobrać checkbox
            pass
        elif token.startswith("miejsce zamieszkania"):
            pass
    return orderer_data


def get_city_data(city_section: list[str]):
    city_data = {}
    for token in city_section:
        token = token.lower()
        if token.startswith("nazwa miasta"):
            city_data["name"] = token.split(":")[1].strip()
        elif token.startswith("adres"):
            splitted = token.split(":")[1].strip().split(",")
            city_data["street"] = splitted[0].strip()
            city_data["local number"] = splitted[1].strip()
        elif token.startswith("zatrudnienie"):
            city_data["job"] = token.split(":")[1].strip()
        elif token.startswith("reprezentowany"):
            city_data["guild"] = token.split(":")[1].strip()
    return city_data

def get_village_data(village_section: list[str]):
    village_data = {}
    for token in village_section:
        token = token.lower()
        if token.startswith("nazwa wsi"):
            village_data["name"] = token.split(":")[1].strip()
        elif token.startswith("zajęcie"):
            village_data["job"] = token.split(":")[1].strip()
        elif token.startswith("adres kontaktowy"):
            splitted = token.split(":")[1].strip().split(",")
            village_data["village head"] = splitted[0].strip()
            village_data["home number"] = splitted[1].strip()
    return village_data

def get_witcher_data(witcher_section : list[str]):
    witcher_data ={}
    for token in witcher_section:
        token = token.lower()
        if token.startswith("imię lub przydomek"):
            witcher_data["name"] = token.split(":")[1].strip()
        elif token.startswith("szkoła wiedźmińska"):
            witcher_data["witcher school"] = token.split(":")[1].strip()
    return witcher_data

def get_details_data(details_section : list[str]):
    details_data ={}
    for token in details_section:
        token = token.lower()
        if token.startswith("gatunek potwora"):
            details_data["monster specie"] = token.split(":")[1].strip()
        elif token.startswith("szkoła wiedźmińska"):
            details_data["witcher school"] = token.split(":")[1].strip()
    return details_data
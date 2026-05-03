import re

def extract_document_summary(text):
    text = text.replace("\n", " ")

    data = {
        "execution": {
            "date": None,
            "place": None,
            "method": "Registered Agreement"
        },
        "licensor": {"names": []},
        "licensees": {"names": []},
        "witnesses": {"names": []}
    }

    # Execution Date & Place
    match = re.search(r"executed on (\d{2}/\d{2}/\d{4}) at ([A-Za-z ]+)", text, re.IGNORECASE)
    if match:
        data["execution"]["date"] = match.group(1)
        data["execution"]["place"] = match.group(2)

    # Licensor
    licensor_match = re.findall(r"Name:\s*Mr\.?\s*([A-Za-z ]+).*?Licensor", text, re.IGNORECASE)
    if licensor_match:
        data["licensor"]["names"] = licensor_match[:1]

    # Licensees
    licensees = re.findall(r"Name:\s*Mr\.?\s*([A-Za-z ]+)", text)
    if licensees:
        data["licensees"]["names"] = licensees[1:]  # skip first (licensor)

    # Witness
    witnesses = re.findall(r"Witness.*?\n([A-Za-z ]+)", text)
    if witnesses:
        data["witnesses"]["names"] = witnesses

    return data
import phonenumbers


def format_phone(phone_number):
    """
    Takes an unformatted phone number, e.g. 8572079431
    and turns it into 857-207-9431
    """
    if not phone_number:
        return ""

    parsed = phonenumbers.parse(phone_number, "US")
    formatted = phonenumbers.format_number(
        parsed,
        phonenumbers.PhoneNumber()
    )
    return formatted

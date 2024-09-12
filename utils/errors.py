def build_error_message(errors: dict):
    """
    Only except serializer errors
    """
    error_string = ""
    for field_name, field_error in errors.items():
        temp_error = ""
        for field_value in field_error:
            temp_error += field_value + " "
        error_string += " " + temp_error
    return error_string

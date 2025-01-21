


class EntryValidation:
    def entry_validation(entries: dict):
        text_list = []

        for key, value in entries.items():

            if key == "warehouse_id" and not value:
                text_list.append("Warehouse")

            elif key == "ref_number" and not value:
                text_list.append("Reference Number")

            elif key == "rm_code_id" and not value:
                text_list.append("Raw Material")

            elif key == "qty_kg" and not value:
                text_list.append("Quantity")

            elif key == "outgoing_date" and not value:
                text_list.append("Outgoing Date")
        return text_list

    # Validation function for numeric input
    def validate_numeric_input(input_value):
        """
        Validates that the input contains only numeric characters.
        """
        return input_value.isdigit() or input_value == ""  # Allow digits or empty input
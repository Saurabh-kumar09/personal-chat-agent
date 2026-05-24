from integrations.sheets_config import sheet


def save_text_to_sheet(user_input):
    getSheet = sheet.get_worksheet(1)
    getSheet.append_row([user_input])

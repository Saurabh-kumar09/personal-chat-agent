from integrations.sheets_config import sheet


def save_text_to_sheet(user_input):
    worksheet = sheet.get_worksheet(1)
    worksheet.append_row([user_input])

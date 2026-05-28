from integrations.sheets_config import sheet


def add_thoughts_to_sheet(user_input):
    worksheet = sheet.get_worksheet(1)
    worksheet.append_row([user_input])


def add_todo_to_sheet(todo_item):
    worksheet = sheet.get_worksheet(2)
    worksheet.append_row([todo_item])

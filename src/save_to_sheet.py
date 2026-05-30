from integrations.sheets_config import sheet


def add_thoughts_to_sheet(user_input):
    worksheet = sheet.get_worksheet(1)
    worksheet.append_row([user_input])


def add_todo_to_sheet(todo_item):
    worksheet = sheet.get_worksheet(2)
    worksheet.append_row([todo_item])


def add_url_to_sheet(url, keyword):
    worksheet = sheet.get_worksheet(3)
    if url in worksheet.col_values(1):
        print(f"URL '{url}' already exists in the sheet.")
        return
    else:
        worksheet.append_row([url, keyword])

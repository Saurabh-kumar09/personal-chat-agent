from integrations.sheets_config import sheet

"""Functions to save content to Google Sheets"""


def add_thoughts_to_sheet(user_input):
    try:
        worksheet = sheet.get_worksheet(1)
        worksheet.append_row([user_input])

    except Exception as error:
        print(f"Failed to save thought: {error}")


def add_todo_to_sheet(todo_item):
    try:
        worksheet = sheet.get_worksheet(2)
        worksheet.append_row([todo_item])

    except Exception as error:
        print(f"Failed to save todo: {error}")


def add_url_to_sheet(url, keyword):
    try:
        worksheet = sheet.get_worksheet(3)

        if url in worksheet.col_values(1):
            print(f"URL '{url}' already exists in the sheet.")
            return

        worksheet.append_row([url, keyword])

    except Exception as error:
        print(f"Failed to save URL: {error}")

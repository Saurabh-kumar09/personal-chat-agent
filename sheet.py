import gspread
from google.oauth2.service_account import Credentials

# Define scope
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Load credentials
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)
# sheet = client.create("dummy_sheet").sheet1
# sheet = client.open("dummy_sheet").sheet1
# sheet.update([[1, 2], [3, 4]], "A1")
# print(sheet.get_all_values())
sheet = client.open_by_key("____")  # connected
print("Connected successfully!")
# values_update
# sheet1 = sheet.values_update(
#     "A1",
#     params={"valueInputOption": "USER_ENTERED"},
#     body={"values": [["Hello, Google Sheets!"]]}
# )

# add worksheet
# sheet.add_worksheet(title="Conversation", rows="100", cols="2")

# append row
# sheet.get_worksheet(0).append_row(["User", "Agent"])
# sheet.add_worksheet(title="Questions", rows="100", cols="2")
# sheet.get_worksheet(2).append_row(["Questions","Topic"])
# sheet.get_worksheet(2).append_row(["What is AI?", "Artificial Intelligence"])

# get values
# sheet.values_get("A1:B2")
# print(sheet.get_worksheet(2).get_values("A2"))
# sheet.get_worksheet(2).append_row(["explain the difference between 0 and 1", "binary"])
# print("Added question to sheet")

# delete worksheet or rows
# sheet.del_worksheet(sheet.get_worksheet(0)) #deletes the conversation sheet
# sheet.get_worksheet_by_id(1388824172).delete_rows(4) #deletes the 4th row in the questions sheet
# sheet.get_worksheet(0).delete_columns(2)
# print("Deleted the second column in the conversation sheet")

# list available sheets
# sheets = sheet.worksheets()
# print("Available sheets:")
# for s in sheets:
#     print(f" - {s.title}")

sheets = sheet.worksheets()
if "Questions" in [s.title for s in sheets]:
    questions_sheet = sheet.worksheet("Questions")
    print("Questions sheet found and accessed.")
else:
    print("Questions sheet not found.")

# append user input to sheet
getSheet = sheet.get_worksheet(0)
user_input = input("you: ")
getSheet.append_row([user_input])

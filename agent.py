from integrations.gemini_config import client
from integrations.sheets_config import sheet

print("""Chat Agent Started
      Hello, How can I assist you today? 
      Type 'exit' to stop the conversation""")

# list stores inputs and responses during the execution of your program
conversation = []

while True:  # infinite loop to keep the conversation going until the user types 'exit'

    getSheet = sheet.get_worksheet(0)
    user_input = input("you: ")
    if user_input.lower() != "exit":
        # do not add "exit" command in sheet
        ques = getSheet.append_row([user_input])
        conversation.append(user_input)
    else:
        print("Conversation ended.")
        break

    # Makes an API request to generate content using a model, passing the conversation history as input.
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=conversation,
    )

    # Returns the concatenation of all text parts in the response.
    reply = response.text
    print("Agent:", reply)

    conversation.append(reply)
    print("Conversation so far:", conversation)

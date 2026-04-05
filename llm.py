import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
os.environ["GEMINI_API_KEY"] = "____"


# value = 5
# print(value)
# print(os.getenv("value_variable"))
# print(os.getenv("GEMINI_API_KEY"))

# Initialize the GenAI client with the API key from environment variables
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# response = client.models.generate_content(
#     model="gemini-3-flash-preview",
#     contents="What's the difference between 0 & 1?"
# )

# print(response.text)

print("Chat Agent Started (type 'exit' to stop)")

# list stores inputs and responses during the execution of your program
conversation = []

while True:

    user_input = input("You: ")

    # type exit to stop the conversation
    if user_input.lower() == "exit":
        break

    conversation.append(user_input)

    # Makes an API request to generate content using a model, passing the conversation history as input.
    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=conversation
    )

    # Returns the concatenation of all text parts in the response.
    reply = response.text
    print("Agent:", reply)

    conversation.append(reply)
    print("Conversation so far:", conversation)

    # Integrate google sheets

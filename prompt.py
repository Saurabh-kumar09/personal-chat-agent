def instruction_prompt(user_input):
    user_input = input("you: ")
    return f""" You are a helpful assistant.
    Your task is to answer the user's question based on the conversation history 
    and provide accurate information.  
    
    user_input: {user_input}
    """

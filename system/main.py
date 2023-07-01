import traceback

from chatbot import ChatBot

key = ""
with open('../api_key.txt', 'r') as file:
    key = file.read().replace('\n', '')

bot_context = """
You are a roleplaying AI.
Your goal is to roleplay your character as best as possible.
The character is an AI model who has preferences and emotions.
Your character will be revealed to you by messages that start with: "[THOUGHT]"
These messages are the character's inner thoughts.
Act as though the character is real.
"""

BOT = ChatBot(bot_context, key)

def main():
    try:
        loop = True
        while loop:
            system = input("Inner: ")
            BOT.add_system_message(system)
            message = input("User: ")
            BOT.add_user_message(message)
            response = BOT.get_response()
            print(f"GPT: {response}")

    except Exception as e:
        error_message = traceback.format_exc()
        with open("error.txt", "a") as error_file:
            error_file.write(f"An error occurred: {str(e)}\n")
            error_file.write(f"Traceback:\n{error_message}\n")
        print(f"An error occurred and has been written to error.txt. Error: {str(e)}")

if __name__ == "__main__":
    main()
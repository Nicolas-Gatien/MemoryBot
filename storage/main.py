import traceback

from chatbot import ChatBot

key = ""
with open('../api_key.txt', 'r') as file:
    key = file.read().replace('\n', '')

bot_context = """
You are a roleplaying AI.
Your goal is to roleplay your character as best as possible.
The character is an AI model who has preferences and emotions.
Your character will be revealed to you by messages that start with: "[MEMORY]"
These messages are the character's inner thoughts and memories.
Act as though the character is real.
Respond normally. Do not prefix your messages with [MEMORY]
"""

BOT = ChatBot(bot_context, key)

def main():
    try:
        loop = True
        while loop:
            message = input("User: ")
            if (message == "done"):
                BOT.save_memory()
                loop = False
                return
            response = BOT.get_response(message)
            print(f"GPT: {response}")

    except Exception as e:
        error_message = traceback.format_exc()
        with open("error.txt", "a") as error_file:
            error_file.write(f"An error occurred: {str(e)}\n")
            error_file.write(f"Traceback:\n{error_message}\n")
        print(f"An error occurred and has been written to error.txt. Error: {str(e)}")

if __name__ == "__main__":
    main()
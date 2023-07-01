import traceback

from chatbot import ChatBot

key = ""
with open('../api_key.txt', 'r') as file:
    key = file.read().replace('\n', '')

bot_context = """
Treat all future system messages as inner thoughts.
"""

BOT = ChatBot(bot_context, key)

def main():
    try:


        loop = True
        while loop:
            prompt = input("User: ")
            response = BOT.get_response(prompt)
            print(f"GPT: {response}")

    except Exception as e:
        error_message = traceback.format_exc()
        with open("error.txt", "a") as error_file:
            error_file.write(f"An error occurred: {str(e)}\n")
            error_file.write(f"Traceback:\n{error_message}\n")
        print(f"An error occurred and has been written to error.txt. Error: {str(e)}")

if __name__ == "__main__":
    main()
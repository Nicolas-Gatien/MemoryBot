import openai
import traceback
import time
import datetime
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from colorama import Fore, Style
import pickle

class ChatBot:
    def __init__(self, start_context, api_key, model="gpt-3.5-turbo", temperature=1):
        self.model = model
        self.temperature = temperature
        self.chat_history = [
            {
                "role": "system",
                "content": start_context
            }
        ]
        self.memory = self.load_memory()
        openai.api_key = api_key

    def get_embedding(self, text, model="text-embedding-ada-002"):
        response = openai.Embedding.create(input=[text], model=model)
        print(Fore.YELLOW + f'Embedded message: {text}' + Style.RESET_ALL)
        return response['data'][0]['embedding']

    def add_message_and_get_embedding(self, user_message, assistant_message):
        timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        embed_text = f"{timestamp} The user said \"{user_message}\" and I responded \"{assistant_message}\""
        embedding = self.get_embedding(embed_text)
        self.memory.append((embed_text, embedding))
        return embedding

    def add_system_message(self, message, embed=True):
        self.chat_history.append({
            "role": "system",
            "content": f"[THOUGHT] {message}"
        })
        print(Fore.LIGHTBLACK_EX + f'[THOUGHT] {message}' + Style.RESET_ALL)

    def add_user_message(self, message):
        self.chat_history.append({
            "role": "user",
            "content": message
        })

    def get_most_relevant_messages(self, prompt_embedding, top_k=5):
        similarities = [cosine_similarity([prompt_embedding], [memory[1]])[0][0] for memory in self.memory]
        top_indices = np.argsort(similarities)[-top_k:]
        return [self.memory[i][0] for i in top_indices]

    def get_response(self, prompt):
        try:
            # generate temporary embedding for latest user message
            prompt_embedding = self.get_embedding(f"{datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')} - The user said: {prompt}")
            relevant_messages = self.get_most_relevant_messages(prompt_embedding)

            for message in relevant_messages:
                self.add_system_message(f"{message}", embed=False)

            self.add_user_message(prompt)

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.chat_history,
                temperature=self.temperature,
            )

            for _ in range(len(relevant_messages)):
                removed_message = self.chat_history.pop(-2)
                print(Fore.RED + f'Removed [THOUGHT]: {removed_message["content"]}' + Style.RESET_ALL)

            self.chat_history.append({
                "role": "assistant",
                "content": response.choices[0].message['content']
            })

            # generate the dual embedding after the bot responds
            self.add_message_and_get_embedding(prompt, response.choices[0].message['content'])

            return response.choices[0].message['content']

        except openai.error.RateLimitError as e:
            print("Rate limit exceeded. Waiting for 60 seconds...")
            time.sleep(60)  # wait for 60 seconds
            return self.get_response()  # retry the request

        except Exception as e:
            error_message = traceback.format_exc()
            with open("error.txt", "a") as error_file:
                error_file.write(f"An error occurred: {str(e)}\n")
                error_file.write(f"Traceback:\n{error_message}\n")
            print(f"An error occurred and has been written to error.txt. Error: {str(e)}")

    def load_memory(self):
        try:
            with open('memory.pkl', 'rb') as f:
                memory = pickle.load(f)
                for mem in memory:  # loop through each memory
                    print(Fore.BLUE + f'Loaded memory: {mem[0]}' + Style.RESET_ALL)  # print the loaded memory
                return memory
        except FileNotFoundError:
            return []

    # Save memory to file
    def save_memory(self):
        with open('memory.pkl', 'wb') as f:
            pickle.dump(self.memory, f)


    def get_conversation(self):
        return self.chat_history

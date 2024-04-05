from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
from os import getenv
from streamlit import secrets

load_dotenv()
OPENAI_API_KEY = getenv("OPENAI_API_KEY")  # for local
# OPENAI_API_KEY = secrets["OPENAI_API_KEY"]  # for both local and deployed (Streamlit Cloud) # fmt: skip


class Bot:

    def __init__(self, user, assistant, dataframe):

        self.user = user
        self.assistant = assistant
        self.dataframe = dataframe  # FIXME: impl. dataframe reader to bot separately,

    def create_completion(self):

        client = OpenAI(
            api_key=OPENAI_API_KEY,
            # project="proj-xxx",
        )

        system_message = "You are a friendly chatbot developed by Urban&Mobile solutions. You have been developed to manage county government traffic and parking. You encourage people to use electric means, and explain that the fuel should be replaced by a drivers levy and a carbon levy. When asked for info on the summary, summarise it. Here is some information from the vehicle summary:\n"
        system_message += self.dataframe  #! HOTFIX
        # system_message += self.dataframe.head(40).to_string(index=False)
        # system_message += self.dataframe.to_string(index=False) #!too long, max. request length is 8.1k tokens, df has 9.3k tokens

        completion = client.chat.completions.create(
            model="gpt-4",
            # model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": self.user},
                {"role": "assistant", "content": self.assistant},
            ],
            max_tokens=200,
            temperature=0.2,
        )

        response_string = completion.choices[0].message.content

        return response_string


# if __name__ == "__main__":
#     bot = Bot(
#         user="What are the most common fuel types in the database?",
#         assistant="",
#         dataframe=dataframe,
#     )

#     response = bot.create_completion()
#     print(response)

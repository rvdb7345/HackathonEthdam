"""
Script for all ChatGPT prompting functions.
"""

# Imports
import openai
import our_secrets


class openAI:
    """
    Model to ask questions to OpenAI's model through an API call.
    """

    def __init__(self, openai_model="text-davinci-003"):
        openai.api_key = our_secrets.open_ai_key
        self.openai_model = openai_model
        self.prompt = "NO PROMPT YET"

    def promptify_article(self, source_article, article_length=500):
        # Create a prompt to write a short article on a given source.
        self.prompt = (
            "You are the editor of a super trustworty newsletter "
            + "reporting on the latest developments in crypto."
            + "Consider the following potential source, relating it "
            + "to everything we gave you before, and write an article "
            + f"about it of about {article_length} characters."
            + "If you think the source information is incorrect or untrue, only "
            + "respond with INCORRECT INFORMATION."
            + f"Source artile: {source_article}."
        )

    def promptify_table(self, table_info, insights_length=500):
        # Create a prompt to write a short article on a given source.
        self.prompt = (
            "You are an expert data analyst, specialized in analyzing financial and crypto data. "
            + "Below, I will provide you with a table containing data on crypto. "
            + "Please provide us with valuable insights on the data, interesting to "
            + "investors and general people interested in developments in crypto currencies. "
            + f"Your anwers should be a maximum of around {insights_length} characters."
            + "If you think the source information is incorrect or untrue, only "
            + "respond with INCORRECT INFORMATION."
            + f"Table: {table_info}."
        )

    def request_to_openai(self):
        # Asking the question and getting an answer
        if self.prompt in ["NO PROMPT YET", "INCORRECT INFORMATION"]:
            return self.prompt
        else:
            print(
                "!!!!!!!!!!\n\nTHIS COSTS MONEY\nLIMITED BUDGET AVAILABLE\n\n!!!!!!!!!!"
            )
            response = openai.Completion.create(
                model=self.openai_model,
                prompt=self.prompt,
                temperature=0,
                max_tokens=100,
                # top_p=1,
                # frequency_penalty=0.0,
                # presence_penalty=0.0,
                # stop=["\n"]
            )
            print("Total tokens used: ", response["usage"]["total_tokens"])
            self.response = response["choices"][0]["text"]

    def custom_request_to_openai(self, custom_prompt):
        # Custom version of the request function for testing purposes
        print("!!!!!!!!!!\n\nTHIS COSTS MONEY\nLIMITED BUDGET AVAILABLE\n\n!!!!!!!!!!")
        response = openai.Completion.create(
            model=self.openai_model,
            prompt=custom_prompt,
            temperature=0,
            max_tokens=100,
            # top_p=1,
            # frequency_penalty=0.0,
            # presence_penalty=0.0,
            # stop=["\n"]
        )
        print("Total tokens used: ", response["usage"]["total_tokens"])
        self.response = response["choices"][0]["text"]

    def run(self, information, info_is_table=False):
        # Function to tie everything together and return ChatGPT's wisdom
        if info_is_table:
            self.promptify_table(information)
        else:
            self.promptify_article(information)

        self.request_to_openai()
        return self.response

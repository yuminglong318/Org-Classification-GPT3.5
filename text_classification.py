
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage

chat = ChatOpenAI(model='gpt-3.5-turbo-0613', temperature=1, openai_api_key=OPENAI_API_KEY)

import json
with open("descriptions.json", "r", encoding="utf-8") as f:
    descriptions = json.load(f)
    categories = [key for key in descriptions.keys()]

def get_classification_from_gpt(description, title):

    system_message_template = """You are an AI classifier to classify organizations. You will be given the title and description of an organization from the user. Classify it into the following categories based on the descriptions and your knowledge.
    % CATEGORIES: 
    {categories}

    % DESCRIPTIONS: 
    {descriptions}
    """

    system_message = PromptTemplate(
        input_variables=["categories", "descriptions"],
        template= system_message_template
    ).format(categories=categories, descriptions=descriptions)

    human_message = f"""
    % Title
    {title}
    % Description
    {description}
    """

    output = chat(
        messages=[
            SystemMessage(content=system_message),
            HumanMessage(content=human_message)
        ]
    )

    for category in categories:
        if category in str(output.content):
            return category


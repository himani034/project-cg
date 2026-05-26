import os
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")


def generate_agent_answer(system_prompt, user_question, context):
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"""
User Question:
{user_question}

Retrieved Context:
{context}

Give a short, clear, professional answer.
"""
            }
        ],
        temperature=0.3,
        max_tokens=300
    )

    return response.choices[0].message.content
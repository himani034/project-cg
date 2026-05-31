import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


def generate_agent_answer(system_prompt, user_question, context):
    response = client.chat.completions.create(
        model=MODEL_NAME,
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
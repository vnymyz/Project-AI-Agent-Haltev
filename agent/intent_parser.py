import json
from agent.openai_client import client

# THIS IS THE INTENT PARSER USING OPENAI
# It will parse user messages into structured JSON data
# that can be used to query the employee database
# with specific intents and filters.
# The expected JSON format is defined in the INTENT_PROMPT.
# If the user does not specify certain fields,
# those fields should be set to null.

INTENT_PROMPT = """
Kamu adalah intent parser untuk sistem HR.
Balas HANYA dalam format JSON berikut.

SELALU isi semua field.
Jika tidak ada nilai, isi null.

{
  "intent": "get_all | get_by_name | filter",
  "name": null | string,
  "filters": {
    "kontrak": null | string,
    "posisi": null | string,
    "min_gaji": null | number,
    "max_gaji": null | number
  }
}
"""

def parse_intent(user_message):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": INTENT_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON from OpenAI")

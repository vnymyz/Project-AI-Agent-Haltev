from agent.openai_client import client

def explain_position(name, position):
    prompt = f"""
Jelaskan secara singkat dan profesional pekerjaan seorang {position}
dalam konteks perusahaan, maksimal 2 kalimat.
Gunakan bahasa Indonesia yang natural.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Kamu adalah HR Assistant"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    explanation = response.choices[0].message.content.strip()

    return f"{name} bekerja sebagai {position}. {explanation}"

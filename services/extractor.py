from groq import Groq

def extract_job_info(job_description: str, api_key: str):
    """Extract job title and company name from the job description using Groq API."""
    client = Groq(api_key=api_key)

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Extract job title and company name from the given text. Always respond with valid JSON only, in the format: {\"jobTitle\": \"...\", \"company\": \"...\"}"
            },
            {
                "role": "user",
                "content": f"Job Description: {job_description}"
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        response_format={"type": "json_object"},
        top_p=1,
        stream=False,
        stop=None
    )

    return completion.choices[0].message.content

import os
from dotenv import load_dotenv

from groq import Groq

def getResponseFromAI(question, scanDetail, apikey=None):
    
    if not question or not scanDetail:
        return "Error: Question and scan details must be provided."
    
    apiKey = apikey

    if not apiKey:
        return "No API key provided, using environment variable"

    client = Groq(api_key=apiKey)
    
    prompt = f"Question: {question}\nScan Details: {scanDetail}\nAnswer:"
    
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

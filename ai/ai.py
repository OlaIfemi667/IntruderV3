import os
from dotenv import load_dotenv

from groq import Groq

def getResponseFromAI(question, scanDetail):

    """
    Function to get a response from OpenAI's API based on the question and scan details.
    """


    load_dotenv() #Pour charger les variables d'environnement depuis le fichier .env
    client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
    print("Using Groq API Key:", os.environ.get("GROQ_API_KEY"))
    if not question or not scanDetail:
        return "Error: Question and scan details must be provided."
    if not os.environ.get("GROQ_API_KEY"):
        return "Error: GROQ_API_KEY environment variable is not set."
    # Prepare the prompt for the AI
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
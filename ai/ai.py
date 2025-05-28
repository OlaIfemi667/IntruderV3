from openai import OpenAI
import os
def getResponseFromAI(question, scanDetail):
    """
    Function to get a response from OpenAI's API based on the question and scan details.
    """
    client = OpenAI(
        #os.environ.get("OPENAI_API_KEY") i have to find a way to do this
        api_key="",
        )
    
    # Prepare the prompt for the AI
    prompt = f"Question: {question}\nScan Details: {scanDetail}\nAnswer:"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
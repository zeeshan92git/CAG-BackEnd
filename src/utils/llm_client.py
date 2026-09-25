############################################################################
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_llm_response(context: str, query: str) -> str:
    """
    Sends the extracted PDF context and user query to Groq LLM and returns the response.
    
    Args:
        context (str): The extracted text content from the PDF
        query (str): The user's question about the PDF content
        
    Returns:
        str: The LLM's response based on the context and query
    """
    try:
        # Get API key from environment variable
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return "Error: GROQ_API_KEY not found in environment variables"
        
        # Initialize Groq client
        client = Groq(api_key=api_key)
        
        # Structure the prompt
        prompt = f"""
        Document Context:
        ---
        {context}
        ---
        
        User Question: {query}
        
        Please answer the user's question using ONLY the information from the document context above.
        If the answer cannot be found in the text, politely state that.
        """
        
        # Call Groq API with Mixtral model (faster, free)
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",  # Fast, free model
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Answer questions based only on the provided document context. Be concise and accurate."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # Lower temperature for factual answers
            max_tokens=1024
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error processing query: {str(e)}"
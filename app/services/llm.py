from typing import List
import openai
from app.core.config import settings
from fastapi import HTTPException

# Initialize OpenAI client (v1 style)
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_answer(query: str, context: List[str]) -> str:
    """
    Generate an answer using OpenAI ChatCompletion based only on the provided context.
    """
    if not context:
        return "I don't know (no relevant context found)."

    # 1. Combine retrieved chunks into a single context string
    formatted_context = "\n\n---\n\n".join(context)

    # 2. Construct the prompt
    prompt = f"""
    You are a professional assistant analyzing the following context to answer a user's question.
    
    Guidelines:
    1. Use the provided context to answer the question as accurately and insightfully as possible.
    2. You are encouraged to perform basic reasoning, calculations (like total years of experience), and synthesis if the evidence is present in the context.
    3. If the answer is absolutely not in the context and cannot be reasonably inferred, say 'I don't know'.

    Context:
    {formatted_context}

    Question:
    {query}
    """

    try:
        # 3. Call OpenAI ChatCompletion API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a RAG system."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,  # Keep it deterministic
        )

        # 4. Extract and return the answer
        return response.choices[0].message.content.strip()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating answer from LLM: {str(e)}"
        )

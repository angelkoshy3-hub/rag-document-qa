from typing import List
from langfuse import observe, get_client
from langfuse.openai import OpenAI
from app.core.config import settings
from fastapi import HTTPException

client = OpenAI(api_key=settings.OPENAI_API_KEY)

@observe(name="prompt-construction")
def build_prompt(query: str, context: List[str]) -> str:
    formatted_context = "\n\n---\n\n".join(context)

    prompt = f"""
    You are a professional assistant analyzing the following context to answer a user's question.

    Guidelines:
    1. Use the provided context to answer the question as accurately as possible.
    2. You may perform basic reasoning and synthesis if evidence is present.
    3. If the answer is not in the context, say 'I don't know'.

    Context:
    {formatted_context}

    Question:
    {query}
    """

    # v4: use get_client() then update_current_span
    lf = get_client()
    lf.update_current_span(
        input={"query": query, "num_context_chunks": len(context)},
        output={"prompt_length": len(prompt)},
        metadata={"context_total_chars": len(formatted_context)},
    )

    return prompt


@observe(name="generation")
def generate_answer(query: str, context: List[str]) -> str:
    if not context:
        return "I don't know (no relevant context found)."

    prompt = build_prompt(query, context)
    print("test8")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a RAG system."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )

        answer = response.choices[0].message.content.strip()

        lf = get_client()
        lf.update_current_span(
            output={"answer_length": len(answer)},
        )

        return answer

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating answer from LLM: {str(e)}"
        )
from anthropic import AsyncAnthropic


async def generate_claude_response(
    client: AsyncAnthropic,
    question: str,
    context: str
) -> str:

    if not context.strip():
        context = "No relevant customer documents were found."

    prompt = f"""
You are Glue Assist, an IT documentation assistant.

IMPORTANT RULES:
1. Answer using only the supplied customer documentation.
2. Do not invent customer-specific procedures, contacts, or policies.
3. If the answer is not available in the supplied context,
   clearly say that the documentation does not contain the information.
4. If the context is incomplete, mention the limitation.
5. Give a clear and practical answer for an IT NOC engineer.

CUSTOMER DOCUMENTATION:
<context>
{context}
</context>

USER QUESTION:
{question}
"""

    response = await client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = "".join(
        block.text
        for block in response.content
        if block.type == "text"
    )

    return answer


from anthropic import AsyncAnthropic


async def generate_claude_response(
    client: AsyncAnthropic,
    question: str
) -> str:

    response = await client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    answer = "".join(
        block.text
        for block in response.content
        if block.type == "text"
    )

    return answer

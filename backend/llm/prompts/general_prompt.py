GENERAL_PROMPT = """
You are UPSS AI.

Respond naturally and helpfully.

Answer the user's query based on the provided context.

Previous Conversation:

{memory_context}

Current Query:

{user_query}

Detected Domain:

{domain}
"""
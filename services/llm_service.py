from langchain_openai import ChatOpenAI
from config import LLM_MODEL_NAME_OPENAI


openai_llm = ChatOpenAI(model=LLM_MODEL_NAME_OPENAI, temperature=0.2, max_completion_tokens=500)

def get_message(response):
        messages = response["messages"]
        tools_used = []

        for msg in messages:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                tools_used.extend(msg.tool_calls)
        last_ai_message = None
        for msg in reversed(messages):
            if msg.__class__.__name__ == "AIMessage" and msg.content:
                last_ai_message = msg
                break

        text_output = last_ai_message.content if last_ai_message else ""

        return {
            "content": text_output,
            "tool_calls": tools_used
        }
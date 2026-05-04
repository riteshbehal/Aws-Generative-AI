# chatbot_backend.py

from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
from langchain_aws import ChatBedrockConverse

# 1. Initialize LLM once (reuse everywhere)
def get_llm():
    return ChatBedrockConverse(
        credentials_profile_name="default",
        model="amazon.nova-pro-v1:0",
        temperature=0.3,
        max_tokens=1000
    )

# 2. Memory setup
def get_memory():
    llm = get_llm()
    return ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=2000,
        return_messages=True
    )

# 3. Conversation handler
def generate_response(input_text, memory):
    llm = get_llm()

    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=False
    )

    # Updated invoke format
    response = conversation.invoke({"input": input_text})

    return response["response"]
#1 import the ConversationSummaryBufferMemory, ConversationChain, ChatBedrock or ChatBedrockConverse Langchain Modules
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
from langchain_aws import ChatBedrockConverse
#2a Write a function for invoking model- client connection with Bedrock with profile, model_id & Inference params- model_kwargs
def demo_chatbot():
    demo_llm=ChatBedrockConverse(
        credentials_profile_name='default',
        model="cohere.command-light-text-v14",
        temperature=0.1,
        max_tokens=1000)
    return demo_llm
#3 Create a Function for ConversationBufferMemory (llm and max token limit)
def demo_memory():
    llm_data=demo_chatbot()
    memory=ConversationSummaryBufferMemory(llm=llm_data,max_token_limit=2000)
    return memory
#4 Create a Function for Conversation Chain - Input text + Memory

def demo_conversation(input_text,memory):
    llm_chain_data=demo_chatbot()
    llm_conversation = ConversationChain(
    llm=llm_chain_data, 
    memory=memory,
    verbose=True
)
#5 Chat response using invoke (Prompt template)
    chat_reply=llm_conversation.invoke(input_text)
    return chat_reply['response']
    


#Links :
#https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html
#https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-runtime_example_bedrock-runtime_Converse_AmazonTitanText_section.html
#https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-deepseek.html


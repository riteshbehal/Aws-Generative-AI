# 1. Import: loader, splitter, Bedrock embeddings + chat model, vector store, and chains
import os
import boto3
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings, ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
 
#5c. Wrap within a function
def hr_index():
    # 2. Load the HR policy PDF from URL
    data_load = PyPDFLoader("https://www.upl-ltd.com/images/people/downloads/Leave-Policy-India.pdf")
    documents = data_load.load()

    # 3. Split text into chunks for embeddings
    data_split = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=500,
        chunk_overlap=50,
    )
    split_docs = data_split.split_documents(documents)

    # 4. Create embeddings client
    data_embeddings = BedrockEmbeddings(
        model_id=os.getenv("BEDROCK_EMBED_MODEL", "amazon.titan-embed-text-v2:0"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    # 5. Build vector store and return it for retrieval
    vector_store = FAISS.from_documents(split_docs, data_embeddings)
    return vector_store
#6a. Write a function to connect to Bedrock Foundation Model - Claude Foundation Model
def hr_llm():
    region = os.getenv("AWS_REGION", "us-east-1")
    bedrock_client = boto3.client("bedrock-runtime", region_name=region)
    llm = ChatBedrock(
        client=bedrock_client,
        model_id=os.getenv("BEDROCK_CHAT_MODEL", "amazon.nova-pro-v1:0"),
        model_kwargs={
            "max_tokens": 1000,
            "temperature": 0.1,
            "top_p": 0.9,
        },
    )
    return llm
#6b. Write a function which searches the user prompt, searches the best match from Vector DB and sends both to LLM.
def hr_rag_response(index, question):
    rag_llm = hr_llm()
    retriever = index.as_retriever(search_kwargs={"k": 4})

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an HR policy assistant. Use the provided context to answer the question."
                " If the answer is not in the context, say you do not know.",
            ),
            ("human", "Question: {input}\n\nContext:\n{context}"),
        ]
    )

    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)
    messages = prompt.format_messages(input=question, context=context)
    result = rag_llm.invoke(messages)
    return getattr(result, "content", str(result))
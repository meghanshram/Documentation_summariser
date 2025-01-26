import os
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv



def initialize_openai_client():
    """
    Initializes the Azure OpenAI client using LangChain's wrapper.
    Ensure API credentials are set as environment variables.
    """
    # Retrieve Azure OpenAI credentials from environment variables
    load_dotenv()
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    if not all([api_key, endpoint, deployment_name]):
        raise ValueError("Azure OpenAI credentials are not properly set in environment variables.")
    
    # Initialize and return the LLM client
    llm = AzureChatOpenAI(
        azure_deployment=deployment_name,
        azure_endpoint=endpoint,
        openai_api_key=api_key,
        openai_api_version="2024-02-01",
        temperature=0.3  # Adjust temperature for response randomness
    )
    return llm

if __name__ == "__main__":
    llm=initialize_openai_client()
    print(llm.invoke("hi"))
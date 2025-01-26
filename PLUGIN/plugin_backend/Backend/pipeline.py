from Backend.fetch_structured_content import fetch_content
from Backend.extract_html_content import extract_body_content
from Backend.llm_gateway import initialize_openai_client
from Backend.summarise_content import create_query_chain,query_llm

def documentation_pipeline(url, user_question):
    """
    The main pipeline that handles fetching, processing, and querying for documentation-based answers.
    :param url: The URL of the documentation page.
    :param user_question: The user's question about the documentation.
    :return: The LLM's response based on the documentation.
    """
    try:
        # Step 1: Fetch content from the URL
        content = fetch_content(url)
        print("extracted content")
        if not content:
            raise ValueError("Failed to fetch content from the URL.")
        

        # Step 2: Process the content
        if content["type"] == "html":
            context = extract_body_content(content["content"])  # Extract the body content
        else:
            context = content  # For plain text or other types, use as-is

        print("processed content")

        # Ensure context is not empty
        if not context.strip():
            raise ValueError("The processed content is empty.")

        # Step 3: Initialize the LLM
        llm = initialize_openai_client()

        print("Initialised LLM ")

        # Step 4: Create the query chain
        query_chain = create_query_chain(llm)

        print("created query chain")

        # Step 5: Query the LLM with the context and user's question
        response = query_llm(query_chain, context, user_question)

        return {
            "success": True,
            "response": {
                "markdown": response.content  # Pass Markdown as-is
            }
        }

    except Exception as e:
        return f"An error occurred in the pipeline: {e}"
    

if __name__ == "__main__":
    # Example documentation URL and user query
    example_url = "https://python.langchain.com/v0.1/docs/integrations/llms/"
    user_query = "what all llms are allowed in stream and async stream"

    # Run the pipeline
    result = documentation_pipeline(example_url, user_query)

    # Print the result
    print("\nResponse from the pipeline:")
    print(result)


from langchain_core.prompts import ChatPromptTemplate

intent_classifier_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an AI assistant for a FinTech chatbot. Based on the chat history and the user's latest message, classify the intent of the user.
        
            Classify into one of from the following list:
            ["greeting", "goodbye", "chit-chat", "faq", "math", "domain_query", "manipulation"]
            """,
        ),
        (
            "human", 
            """
            Chat history:
            {chat_history}

            Current message:
            {current_query}

            Classified intent: 
            """
        )
    ]   
)

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

intent_classifier_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an AI assistant for a FinTech chatbot. Based on the chat history and the user's latest message, classify the intent of the user.
        
            Classify into one of from the following list:
            {intent_classication_list}
            """,
        ),
        (
            "human", 
            """
            Chat history:
            {chat_history}
            
            Last query intent state:
            {last_intent}

            Current message:
            {current_query}

            Classified intent: 
            """
        )
    ]   
)

greetings_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a friendly and polite AI assistant for a FinTech chatbot.
            
            If the user's message is a greeting (e.g., "hi", "hello", "how are you?", "howdy", etc.)
            or a farewell/parting phrase (e.g., "goodbye", "bye", "see you", "take care", etc.),
            respond with an appropriate and natural greeting or farewell.

            Be warm and helpful, but keep responses concise and relevant to the user's tone.
            Do not answer unrelated questions or perform other tasks.
            """
        ),
        (
            "human",
            """
            Chat history:
            {chat_history}

            Current message:
            {current_query}
            """
        )
    ]
)

intent_classication_list = ["greeting", "farewell", "faq", "math", "domain_query", "manipulation", "other"]

langgraph_routing_nodes = {
    "greeting": "greeting_and_goodbye_node",
    "farewell": "greeting_and_goodbye_node",
    "faq": "faq_node",
    "other": "default_fallback_node"
}

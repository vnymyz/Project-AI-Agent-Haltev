from agent.legacy_agent import ai_agent

# FALLBACK ML AGENT USING LEGACY CODE IN CASE OPENAI FAILS

def ml_fallback(user_message):
    return ai_agent(user_message)

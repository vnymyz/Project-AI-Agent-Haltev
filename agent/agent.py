from agent.intent_parser import parse_intent
from agent.query_engine import query_employee
from agent.table_renderer import render_table
from agent.fallback_ml import ml_fallback

# THIS IS FOR THE PRIMARY AGENT THAT USES OPENAI

# def handle_message(user_message: str):
#     """
#     Primary AI Agent (OpenAI-based)
#     """
#     try:
#         intent_data = parse_intent(user_message)
#         df_result = query_employee(intent_data)
#         return render_table(df_result)

#     except Exception as e:
#         # Graceful fallback ke ML lama
#         return ml_fallback(user_message)

# FOR DEV ONLY
def handle_message(user_message: str, debug=False):
    try:
        intent_data = parse_intent(user_message)
        df_result = query_employee(intent_data)
        table = render_table(df_result)

        if debug:
            return {
                "intent": intent_data,
                "response": table
            }

        return table

    except Exception:
        return ml_fallback(user_message)

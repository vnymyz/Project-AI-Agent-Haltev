from agent.intent_parser import parse_intent
from agent.query_engine import query_employee
from agent.table_renderer import (
    render_summary_table,
    render_detail_table
)
from agent.fallback_ml import ml_fallback


def handle_message(user_message: str):
    try:
        intent_data = parse_intent(user_message)
        df_result = query_employee(intent_data)

        # guard tambahan
        if "detail" in user_message.lower() or "lengkap" in user_message.lower():
            return render_detail_table(df_result)

        if intent_data.get("detail"):
            return render_detail_table(df_result)
        else:
            return render_summary_table(df_result)

    except Exception:
        return ml_fallback(user_message)


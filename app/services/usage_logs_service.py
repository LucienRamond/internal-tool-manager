from models.usage_logs import Usage_logs


class UsageLogs():
    def get_usage_logs():
        usage_logs = Usage_logs.query
        return usage_logs
    
    def get_usage_logs_by_tool_id(tool_id):
        usage_logs_query = UsageLogs.get_usage_logs().filter(Usage_logs.tool_id == tool_id).all()

        response = [{
            "id": usage_logs.id,
            "tool_id": usage_logs.tool_id,
            "user_id": usage_logs.user_id,
            "session_date": usage_logs.session_date,
            "usage_minutes": usage_logs.usage_minutes,
            "actions_count": usage_logs.actions_count,
            "created_at": usage_logs.created_at,
        }for usage_logs in usage_logs_query]

        return response

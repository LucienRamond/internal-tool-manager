from models.cost_tracking import Cost_tracking

class CostTracking():
    def get_cost_tracking():
        cost_tracking = Cost_tracking.query
        return cost_tracking
    
    def get_cost_tracking_by_tool_id(tool_id):
        cost_tracking_query = CostTracking.get_cost_tracking().filter(Cost_tracking.tool_id == tool_id)
        cost_tracking = cost_tracking_query[0]

        response = {
            "id": cost_tracking.id,
            "month_year": cost_tracking.month_year,
            "total_monthly_cost": cost_tracking.total_monthly_cost,
            "active_users_count": cost_tracking.active_users_count,
            "created_at": cost_tracking.created_at,
        }

        return response

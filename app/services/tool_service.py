from flask import make_response
from models.cost_tracking import Cost_tracking
from models.categories import Categories
from models.tools import Tools
from main import db
from services.cost_tracking_service import CostTracking

class ToolService():
    def get_tools_with_categories():
        return db.session.query(Tools, Categories).join(Categories)
    
    def get_tool_by_id(id):
        tool_category_query = ToolService.get_tools_with_categories().filter(Tools.id == id).all()
        tool = tool_category_query[0][0]
        category = tool_category_query[0][1]
        cost_tracking = CostTracking.get_cost_tracking_by_tool_id(id)

        response = {
            "id": tool.id,
            "name": tool.name, 
            "description": tool.description,
            "vendor": tool.vendor,
            "website_url": tool.website_url,
            "category": category.name,
            "monthly_cost": tool.monthly_cost,
            "owner_department": tool.owner_department,
            "status": tool.status,
            "active_users_count": cost_tracking["active_users_count"],
            "total_monthly_cost": cost_tracking["total_monthly_cost"],
            "created_at": tool.created_at,
            "updated_at": tool.updated_at,
            "usage_metrics": {
                "last_30_days": {
                "total_sessions": 127,
                "avg_session_minutes": 45
                }
            }
        }

        return make_response(response, 200)


    def get_all_tools(department, status, category, min_cost, max_cost, sort, page, per_page):
        tools_query = ToolService.get_tools_with_categories()
        filters_applied = {}
        total = 0

        if department :
            tools_query = tools_query.filter(Tools.owner_department == department)
            filters_applied.update({"department": department})   

        if status :
            tools_query = tools_query.filter(Tools.status == status)
            filters_applied.update({"status": status})   

        if category :
            tools_query = tools_query.filter(Categories.name == category)
            filters_applied.update({"category": category})   

        if min_cost :
            tools_query = tools_query.filter(Tools.monthly_cost >= float(min_cost))
            filters_applied.update({"min_cost": float(min_cost)})  

        if max_cost :
            tools_query = tools_query.filter(Tools.monthly_cost <= float(max_cost))
            filters_applied.update({"max_cost": float(max_cost)})

        if sort :
            if sort == "name":
                tools_query = tools_query.order_by(Tools.name)
            else:
                tools_query = tools_query.order_by(sort)               
            filters_applied.update({"sorted_by": sort})
        
        if page or per_page:
            tools_query = tools_query.paginate()
            filters_applied.update({"pages":tools_query.pages})
            total = tools_query.total

        tools = [{
            "id": tool.id,
            "name": tool.name,
            "description": tool.description,
            "vendor": tool.vendor,
            "category": categories.name,
            "monthly_cost": tool.monthly_cost,
            "owner_department": tool.owner_department,
            "status": tool.status,
            "website_url": tool.website_url,
            "active_users_count": tool.active_users_count,
            "created_at": tool.created_at,
            
        } for tool, categories in tools_query]

        if not page or not per_page:
            total = len(tools)

        if not len(tools) :
            return make_response({
                "message": "No tools were found based on your filters",
                "total":len(tools),
                'filters_applied':filters_applied
            }, 200)

        return make_response({
            "data": tools,
            "total":total,
            'filtered':len(ToolService.get_tools_with_categories().all()) - len(tools),
            'filters_applied':filters_applied,
        }, 200)
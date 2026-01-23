from functools import reduce
from flask import make_response
from utils.check_functions import check_monthly_cost, check_name_length, check_tools_owner_department, check_tools_status, check_valid_url, check_vendor_length
from utils.globals import OWNER_DEPARTMENT, TWO_DECIMAL_REGEX, VERIFY_DOMAIN_REGEX
from services.usage_logs_service import UsageLogs
from models.categories import Categories
from models.tools import Tools
from main import db
from services.cost_tracking_service import CostTracking
import re

class ToolService():
    def get_tools_with_categories():
        return db.session.query(Tools, Categories).join(Categories)
    
    def create_tool(data):
        website_url = ""
        description = ""
        vendor = ""

        # Check optionnal fields
        if "website_url" in data :
           website_url = data["website_url"]

        if "description" in data :
            description = data["description"]

        # Check required fields
        try :
            name = data["name"]
            monthly_cost = data["monthly_cost"]
            owner_department = data["owner_department"]         
            category_id = data["category_id"]         
            vendor = data["vendor"]         
        except Exception as e :
            return make_response({
                "message": f'le champ {e} est obligatoire'
            }, 400)
        
        tool_category = ToolService.get_tools_with_categories().filter(Categories.id == category_id).first()
        verify_unique_name = ToolService.get_tools_with_categories().filter(Tools.name == name).first()

        # Validation data
        try :
            details = {}

            if check_name_length(name):
                details.update(check_name_length(name))
            
            if len(verify_unique_name) > 0:
                details.update({"Name" : f'{name} already exists'})

            if check_monthly_cost(data["monthly_cost"]):
                details.update(check_monthly_cost(data["monthly_cost"]))

            if check_tools_owner_department(data["owner_department"]):
                details.update(check_tools_owner_department(data["owner_department"]))

            if len(website_url) :
                if check_valid_url(website_url):
                    details.update(check_valid_url(website_url))
                
            if len(tool_category) == 0 :
                details.update({"tool_category" : f"Category with id : {category_id} doesn't exist"})

            if check_vendor_length(vendor) :
                details.update(check_vendor_length(vendor))
            
            if len(details) > 0:
                raise Exception            
        
        except Exception:
            return make_response({
                "error": "Validation failed",
                "details" : details
            }, 400)


        tool = Tools(name=name, 
                     description=description, 
                     vendor=vendor, 
                     website_url=website_url, 
                     category_id=category_id, 
                     monthly_cost=monthly_cost, 
                     owner_department=owner_department)

        db.session.add(tool)
        db.session.commit()

        response = {
            "id": tool.id,
            "name": tool.name,
            "description": tool.description, 
            "vendor": tool.vendor,
            "website_url": tool.website_url,
            "category": tool_category[0][1].name,
            "monthly_cost": tool.monthly_cost,
            "owner_department": tool.owner_department, 
            "status": tool.status,
            "active_users_count": tool.active_users_count,
            "created_at": tool.created_at,
            "updated_at": tool.updated_at
        }
        
        return make_response(response, 201)
    
    def update_tool(tool_id, data):
        tool_query = ToolService.get_tools_with_categories().filter(Tools.id == tool_id).first()

        if not tool_query:
           return make_response({
                "error": "Tool not found",
                "message": f'Tool with ID {tool_id} does not exist'
                }, 404) 

        tool = tool_query[0]
        category = tool_query[1]

        # Check fields
        try :
            details = {}
            if "status" in data:
                if check_tools_status(data["status"]):
                    details.update(check_tools_status(data["status"]))        
                else :
                    tool.status = data["status"]   

            if 'description' in data:
                tool.description = data["description"]                     

            if 'monthly_cost' in data:
                if check_monthly_cost(data["monthly_cost"]):
                    details.update(check_monthly_cost(data["monthly_cost"]))
                else :
                    tool.monthly_cost = data["monthly_cost"]
            
            if len(details) > 0:
                raise Exception
            
        except Exception as e:
            return make_response({
                "error": "Validation failed",
                "details" : details
            }, 400)

        db.session.commit()

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
            "active_users_count": tool.active_users_count,
            "created_at": tool.created_at,
            "updated_at": tool.updated_at
        }

        return make_response(response, 200)
    
    def get_tool_by_id(id):
        tool_category_query = ToolService.get_tools_with_categories().filter(Tools.id == id).first()

        if not tool_category_query:
           return make_response({
                "error": "Tool not found",
                "message": f'Tool with ID {id} does not exist'
                }, 404) 

        tool = tool_category_query[0]
        category = tool_category_query[1]

        cost_tracking = CostTracking.get_cost_tracking_by_tool_id(id)

        # Calculates metrics
        usage_logs = UsageLogs.get_usage_logs_by_tool_id(id)
        total_sessions = 0
        avg_session_minutes = 0
        if usage_logs :
            total_sessions = len(usage_logs)
            for session in usage_logs :
                total_sessions = total_sessions + session["usage_minutes"]
            avg_session_minutes = total_sessions / len(usage_logs)

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
                "total_sessions": total_sessions,
                "avg_session_minutes": avg_session_minutes
                }
            }
        }

        return make_response(response, 200)


    def get_all_tools(department, status, category, min_cost, max_cost, sort, page, per_page):
        tools_query = ToolService.get_tools_with_categories()
        filters_applied = {}
        total = 0

        # Check and apply filters
        # TODO: refactor all these if
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

        # Check and apply sorting
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
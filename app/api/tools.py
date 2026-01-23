from flask import Blueprint, request
from services.tool_service import ToolService

tool_route = Blueprint('band_route', __name__)

@tool_route.route('/api/tools', methods=['GET'])
def get_all_tools():
    department = request.args.get('department')
    status = request.args.get('status')
    category = request.args.get('category')
    min_cost = request.args.get('min_cost')
    max_cost = request.args.get('max_cost')
    sort = request.args.get('sort')
    page = request.args.get('page')
    per_page = request.args.get('per_page')
    return ToolService.get_all_tools(department, status, category, min_cost, max_cost, sort, page, per_page)

@tool_route.route('/api/tools/<int:id>', methods=['GET'])
def get_tool(id):
    return ToolService.get_tool_by_id(id)

@tool_route.route('/api/tools', methods=['POST'])
def create():
    data = request.get_json()
    return ToolService.create_tool(data)
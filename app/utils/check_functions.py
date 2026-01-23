import re
from utils.globals import OWNER_DEPARTMENT, TOOLS_STATUS, TWO_DECIMAL_REGEX, VERIFY_DOMAIN_REGEX

def check_monthly_cost(monthly_cost):
    if not monthly_cost > 0 or not re.match(TWO_DECIMAL_REGEX, str(monthly_cost)):
        return {"monthly_cost" : 'Le coût mensuel doit être superieur à 0 et maximum 2 décimales.'}

def check_valid_url(url):
    if not re.match(VERIFY_DOMAIN_REGEX, url):
        return {"website_url" : "Must be a valid URL format"}

def check_name_length(name):
    if not len(name) >= 2 or not len(name) <= 100:
        return {"Name" : 'Name must be 2-100 characters'}

def check_vendor_length(vendor):
    if len(vendor) > 100 :
        return {"vendor" : "Vendor must be 2-100 characters"}
    
def check_tools_status(status):
    if status not in TOOLS_STATUS:
        return {"status" : "status must be 'active' | 'deprecated' | 'trial'"}
    
def check_tools_owner_department(owner_department):
    if owner_department not in OWNER_DEPARTMENT:
        return {"owner_department" : "Department must be Engineering, Sales, Marketing, HR, Finance, Operations ou Design"}

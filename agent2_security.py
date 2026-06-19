#ToDo: Replace with actual code later, return true for agent1 checking purposes
#from security_monitor import log_attempt, record_failure
#from authorize import authorize
from users import USERS
from access_control import authorize
from security_monitor import log_attempt, record_failure, is_flagged
from datetime import datetime

# access permissions for each agent roles
AGENT_PERMISSIONS = {
   "agent5_payroll": {
       "employee_id",
       "employment_type",
       "base_salary",
       "department"
   },


   "agent4_benefits": {
       "employee_id",
       "employment_type",
       "health_insurance",
       "retirement_contribution",
       "stock_options"
   },


   "agent3_absence": {
       "employee_id",
       "employment_type",
       "department"
   },


   "hr_admin": {
       "*"
   }
}

#checks and authorizes agent depending on it's permissions and depending on the user's permissions
def authorize_request(agent_name, requested_fields):
   #Check whether an agent can access requested fields.
   if agent_name not in AGENT_PERMISSIONS:
       log_agent_access(agent_name,"DENIED","Unknown agent")
       return False

   permissions = AGENT_PERMISSIONS[agent_name]

   if "*" in permissions:
       log_agent_access(agent_name,"APPROVED","Admin access")
       return True

   unauthorized = [
       field for field in requested_fields
       if field not in permissions
   ]

   if unauthorized:
       log_agent_access(agent_name,"DENIED",f"Unauthorized fields: {unauthorized}")
       return False
   log_agent_access(agent_name,"APPROVED","Valid request")
   return True

#runs security check of user and agents, verifies, authorizes, and logs attempt
def run_security_check(user, action, agent_name=None, requested_fields=None):
    if user not in USERS:
        log_attempt(user, action, allowed=False)
        record_failure(user)
        return False

    if is_flagged(user):
        log_attempt(user, action, allowed=False)
        return False
    
    role = USERS[user]["role"]

    if not authorize(role, action):
        log_attempt(user, action, allowed=False)
        record_failure(user)
        return False

    if agent_name and requested_fields:
        if not authorize_request(agent_name, requested_fields):
            return False

    log_attempt(user, action, allowed=True)
    return True

# logs access attempts of agents
AGENT_ACCESS_LOG = []
def log_agent_access(agent_name, status, reason):
   #Records all security decisions.
   AGENT_ACCESS_LOG.append({
       "timestamp": datetime.now(),
       "agent": agent_name,
       "status": status,
       "reason": reason
   })

def get_agent_logs():
   return AGENT_ACCESS_LOG

if __name__ == "__main__":
    print("=== Testing Agent 2 ===")
    
    print("\n1. Valid user, valid action:")
    print(run_security_check("anna.smith", "view_payroll"))
    
    print("\n2. Valid user, action not allowed for their role:")
    print(run_security_check("david.kim", "delete_employee"))
    
    print("\n3. User doesn't exist:")
    print(run_security_check("fake.user", "view_payroll"))
    
    print("\n4. Check audit log recorded these attempts:")
    from security_monitor import get_audit_log
    for entry in get_audit_log():
        print(entry)

"""
# connecting to agent 1: determining access permissions (anonymized or non) for payroll data based on which agent is requesting
def get_employee_data(agent_name, requested_fields):
   approved = authorize_request(
       agent_name,
       requested_fields
   )
   if not approved:
       raise PermissionError(
           f"{agent_name} is not authorized."
       )

   # HR gets full records
   if agent_name == "hr_admin":
       return original_list

   # Other agents get anonymized records
   filtered_records = []

   for employee in anonymized_list:


       filtered = {}


       for field in requested_fields:
           if field in employee:
               filtered[field] = employee[field]


       filtered_records.append(filtered)


   return filtered_records
   """

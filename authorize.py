# agent 1: authorization for payroll data access

from data_loader import USERS
from access_control import authorize
from anonymizer import anonymize_id, anonymized_list
from security_monitor import log_attempt

#for seeing who is trying to access the information. If HR/admin, then can see everyone, if manager, then can see department/team, if only employee, then can only see self
user = input("Enter your employee ID: ")
#may need to have authentification here to verify identity of user (like password/2FA)
user_role = USERS.get(user, {}).get("role", "employee")

if not authorize(user_role, "view_payroll"):
    log_attempt(user, "view_payroll")
    print("Access denied: You do not have permission to view payroll data.")

# for HR/admins
if authorize(user_role, "view_all"):
    print("Access granted: Here is the anonymized payroll data.")
    for record in anonymized_list:
        print(record)

# for managers
elif authorize(user_role, "view_department"):
    print("Access granted: Here is the anonymized payroll data for your department.")
    manager_department = USERS[user]["department"]
    results = []
    for emp in anonymized_list:
        if emp["department"] == manager_department:
            results.append(emp)
    print(results)

# for employees
if authorize(user_role, "view_self"):
    print("Access granted: Here is your anonymized payroll data.")
    for record in anonymized_list:
        if record["employee_id"] == anonymize_id(USERS[user]["employee_id"]):
            print(record)

#logging access attempts for security monitoring and auditing purposes
from security_monitor import log_attempt

#for managers: NEED TO FIX, SO CAN WORK FOR EMPLOYEES TOO
# able to access department
log_attempt(
    user,
    "view_department",
    True
)
#unable to access department
log_attempt(
    user,
    "unauthorized_department_access",
    False
)
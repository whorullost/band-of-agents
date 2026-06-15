# agent 1: authorization for payroll data access

from data_loader import USERS
from access_control import authorize
from anonymizer import anonymize_id, anonymized_list
from security_monitor import log_attempt

#for seeing who is trying to access the information. If HR/admin, then can see everyone, if manager, then can see department/team, if only employee, then can only see self
username = input("Enter your employee ID: ")
user = USERS.get(username)
#need a security check to make sure that user is truely who they are

#if user not found in system, then log attempt and deny access
if user is None:
    log_attempt(username, "view_payroll", False)
    print("Access denied: You do not have permission to view payroll data.")
    exit()

#user found in system, check role and permissions
user_role = USERS.get(user, {}).get("role", "employee")
print(f"Welcome! You are logged in as {username} with role {user_role}.")

#may need search function maybe?

# for HR/admins
if authorize(user, "view_all"):
    log_attempt(username, "view_all", True)
    print("Access granted: Here is the  payroll data for all employees.")
    for record in anonymized_list:
        print(record)

# for managers
elif authorize(user, "view_department"):
    log_attempt(username, "view_department", True)
    print("Access granted: Here is the anonymized payroll data for your department.")
    manager_department = USERS[user]["department"]
    results = []
    for emp in anonymized_list:
        if emp["department"] == manager_department:
            results.append(emp)
    print(results)

# for employees
if authorize(user, "view_self"):
    log_attempt(username, "view_self", True)
    print("Access granted: Here is your anonymized payroll data.")
    for record in anonymized_list:
        if record["employee_id"] == anonymize_id(USERS[user]["employee_id"]):
            print(record)

else:

    log_attempt(username, "view_payroll", False)

    print(
        "Access denied: insufficient permissions"
    )

#logging access attempts for security monitoring and auditing purposes
from security_monitor import log_attempt

#for managers: NEED TO FIX, SO CAN WORK FOR EMPLOYEES TOO
# able to access department
log_attempt(
    username,
    "view_department",
    True
)
#unable to access department
log_attempt(
    username,
    "unauthorized_department_access",
    False
)
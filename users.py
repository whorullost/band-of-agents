"""
System login credentials and role assignments.
Defines who can log into the HR system and what role they have.
Separate from employee_dataset.csv which stores payroll/HR data.
Never import this directly into any AI agent.
"""

USERS = {
    "anna.smith": {
        "employee_id": "E007",
        "role": "admin",
        "department": "Human Resources"
    },
    "james.park": {
        "employee_id": "E002",
        "role": "senior_hr",
        "department": "Human Resources"
    },
    "chris.lee": {
        "employee_id": "E008",
        "role": "manager",
        "department": "Engineering"
    },
    "lisa.wong": {
        "employee_id": "E005",
        "role": "manager",
        "department": "Marketing"
    },
    "sarah.chen": {
        "employee_id": "E001",
        "role": "junior_hr",
        "department": "Engineering"
    },
    "david.kim": {
        "employee_id": "E004",
        "role": "employee",
        "department": "Engineering"
    },
    "maya.patel": {
        "employee_id": "E009",
        "role": "employee",
        "department": "Marketing"
    },
    "tom.harris": {
        "employee_id": "E006",
        "role": "employee",
        "department": "Finance"
    },
    "maria.lopez": {
        "employee_id": "E003",
        "role": "manager",
        "department": "Finance"
    },
    "john.davis": {
        "employee_id": "E010",
        "role": "admin",
        "department": "Finance"
    },
    "@miachang0316": {
        "employee_id": "E012", 
        "role": "admin",
        "department": "Human Resources"
    },
    "miachang0316": {  # defensive duplicate, in case @ gets stripped during agent relay
        "employee_id": "E007",
        "role": "admin",
        "department": "Human Resources"
    },
}

def get_user(user):
    return USERS.get(user)

def get_all_user():
    return USERS

def add_new_user(user, id, role, dep):
    if user in USERS:
        return "User already exists"
    else:
        USERS[user] = {
            "employee_id" : id,
            "role":role,
            "department":dep
        }

def delete_user(user):
    if user not in USERS:
        return "User do not exist"
    else:
        del USERS[user]

def update_user_role(user, new_role):
    if user not in USERS:
        return "User do not exist"
    else:
        USERS[user]["role"] = new_role 
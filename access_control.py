# agent 1: access control for payroll data
"""Defines role permissions and authorization logic.
This is a part of Agent 2's security layer.
WARNING: Never import this directly into any AI agent.

KEY: Roles (lowest to highest access):
    employee   → view own data only
    junior_hr  → view absences only
    manager    → view department data, mark absences
    senior_hr  → view everything, run payroll
    admin      → full access including delete and reidentify
"""


ROLES = {
    "admin": ["view_payroll", "view_reports", "reidentify", "add_employee", "edit_salary", "run_payroll", "delete_employee"],
    "senior_hr": ["view_payroll", "view_reports", "run_payroll", "edit_salary"],
    "manager": ["view_department_reports", "view_department", "mark_absences"],
    "junior_hr": ["view_absences"],
    "employee": ["view_self"]
}

def get_permission(role):
   return ROLES.get(role, [])

def is_valid_role(role):
   return role in ROLES

def authorize(role, action):
   return action in ROLES.get(role, [])




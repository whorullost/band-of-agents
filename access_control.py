# agent 1: access control for payroll data
from data_loader import USERS

ROLES = {
    #Mia's
    "admin": ["view_payroll", "view_reports", "reidentify", "add_employee", "edit_salary", "run_payroll", "delete_employee", "view_audit_log", "view_flagged_users", "mark_absences", "view_self"],
    "senior_hr": ["view_payroll", "view_reports", "run_payroll", "edit_salary", "mark_absences", "view_department_reports", "view_department"],
    "manager": ["view_department_reports", "view_department", "mark_absences"],
    "junior_hr": ["view_absences", "view_self"],
    "employee": ["view_self"]
}


def authorize(user, action):
    role = user["role"]

    allowed_actions = ROLES.get(role, [])

    return action in allowed_actions
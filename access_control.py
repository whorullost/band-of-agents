# agent 1: access control for payroll data
from data_loader import USERS

ROLES = {
    "hr_admin": [
        "view_all",
        "view_payroll",
        "reidentify",
        "view_security_logs"
        "view_self"
    ],

    "manager": [
        "view_department"
        "view_self"
    ],

    "employee": [
        "view_self"
    ]
}


def authorize(user, action):
    role = user["role"]

    allowed_actions = ROLES.get(role, [])

    return action in allowed_actions
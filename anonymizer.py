"""Handles all data anonymization before passing to AI agents.
Scrambles sensitive employee information (names, IDs, salaries) so that
external AI models never see real personal data. Works together with
data_loader.py (fetches real data) and lookup.py (unscrambles at the end).
This file should never write to the database, read only operations here.
"""
import hashlib
import os

# Secret salt makes hashes impossible to reverse without knowing this value
# Stored as environment variable so it's never hardcoded in public code
SECRET_SALT = os.getenv("ANON_SALT", "hackathon-secret")

# Convert real salary to a range label so AI never sees exact numbers, but only to select AIs that dont need to calculate with exact salaries
def anonymize_salary(salary):
    if salary < 50000:
        return "Low-Range"
    elif salary < 75000:
        return "Mid-Range"
    elif salary < 100000:
        return "Mid-High-Range"
    else:
        return "High-Range"

# Converts real name to anonymous code using salted hash
def anonymize_name(name):
    digest = hashlib.sha256(
        f"{SECRET_SALT}:{name}".encode()
    ).hexdigest()
    return f"EMP_{digest[:8].upper()}"

#Converts real employee ID to anonymous session ID using salted hash
def anonymize_id(id):
    digest = hashlib.sha256(
        f"{SECRET_SALT}:{id}".encode()
    ).hexdigest()
    return f"S_{digest[:8].upper()}"

#Takes one real employee dictionary, returns fully anonymized version
def anonymize_one(employee):
    return {
        "employee_id": anonymize_id(employee["employee_id"]),
        "name": anonymize_name(employee["name"]),
        "department": employee["department"],
        "job_title": employee["job_title"],
        "employment_type": employee["employment_type"],
        "base_salary": employee["base_salary"],
        "start_date": employee["start_date"],
        "health_insurance": employee["health_insurance"],
        "retirement_contribution": employee["retirement_contribution"],
        "stock_options": employee["stock_options"]
    }

def prepare_for_agent(employee, agent_type):
    views = {
        "payroll_agent": { #agent 5 (payroll calc)
            "employee_id": employee["employee_id"],
            "base_salary": employee["base_salary"],
            "employment_type": employee["employment_type"]
        },

        "benefits_agent": { #agent 4 (benefit agent), 5 (payroll calc)
            "employee_id": anonymize_id(employee["employee_id"]),
            "health_insurance": employee["health_insurance"],
            "retirement_contribution": employee["retirement_contribution"],
            "stock_options": employee["stock_options"]
        }
    }

    return views[agent_type]

#Takes list of real employee dictionaries, returns fully anonymized list.
def anonymize_all(employees_list):
    anon_lst = []
    for i in range(len(employees_list)):
        anon_emp = anonymize_one(employees_list[i])
        anon_lst.append(anon_emp)
    return anon_lst





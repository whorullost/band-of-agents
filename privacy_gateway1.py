import pandas as pd
import hashlib
import secrets

# Convert real salary to a range label so AI never sees exact numbers
def anonymize_salary(salary):
    if salary < 50000:
        return "Low-Range"
    elif salary < 75000:
        return "Mid-Range"
    elif salary < 100000:
        return "Mid-High-Range"
    else:
        return "High-Range"

# Convert real salary to a range label so AI never sees exact numbers
def anonymize_name(name):
    real_name = name
    ano_name = "EMP_"+ hashlib.sha256(real_name.encode()).hexdigest()[:6].upper()
    return ano_name

# Generate a random session ID so real employee IDs are never exposed
def anonymize_id(id):
    real_id = id
    ano_id = "S_"+ secrets.token_hex(4).upper()
    return ano_id

# Takes one employee's real data and returns fully anonymized version
def anonymize_dataset(employee):
    return {
        "employee_id": anonymize_id(employee["employee_id"]),
        "name": anonymize_name(employee["name"]),
        "department": employee["department"],
        "job_title": employee["job_title"],
        "employment_type": employee["employment_type"],
        "base_salary": anonymize_salary(employee["base_salary"]),
        "start_date": employee["start_date"],
        "health_insurance": employee["health_insurance"],
        "retirement_contribution": employee["retirement_contribution"],
        "stock_options": employee["stock_options"]
    }

def anonymize_all():
    lst = []
    for _, row in df.iterrows():
        employee = row.to_dict()
        lst.append(anonymize_dataset(employee))
    return lst

df = pd.read_csv("employee_dataset.csv")
anonymized_list = anonymize_all()
original_list = []

for _, row in df.iterrows():
        employee = row.to_dict()
        original_list.append(employee)

def build_lookup_table():
    count = 0
    lookup = {}
    for i in range(len(anonymized_list)):
        lookup[anonymized_list[i]["employee_id"]] = original_list[i]["employee_id"]
        lookup[anonymized_list[i]["name"]] = original_list[i]["name"]
    return lookup
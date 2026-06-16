import pandas as pd
from pathlib import Path
from datetime import datetime

ABSENCE_FILE = "absences.csv"

COLUMNS = [
    "employee_id",
    "date",
    "absence_type",
    "hours_missed",
    "region",
    "employment_type"
]


def _initialize_file():
    if not Path(ABSENCE_FILE).exists():
        pd.DataFrame(columns=COLUMNS).to_csv(ABSENCE_FILE, index=False)


_initialize_file()


def record_absence(
    employee_id,
    date,
    absence_type,
    hours_missed,
    region,
    employment_type
):
    """
    Stores only anonymized employee IDs.
    """

    df = pd.read_csv(ABSENCE_FILE)

    new_row = {
        "employee_id": employee_id,
        "date": date,
        "absence_type": absence_type,
        "hours_missed": hours_missed,
        "region": region,
        "employment_type": employment_type
    }

    df.loc[len(df)] = new_row
    df.to_csv(ABSENCE_FILE, index=False)

    return True


def get_absences_by_employee(employee_id):

    df = pd.read_csv(ABSENCE_FILE)

    return df[
        df["employee_id"] == employee_id
    ].to_dict("records")


def get_absences_by_month(month, year):

    df = pd.read_csv(ABSENCE_FILE)

    df["date"] = pd.to_datetime(df["date"])

    results = df[
        (df["date"].dt.month == month)
        & (df["date"].dt.year == year)
    ]

    return results.to_dict("records")


def get_leave_balance(employee_id, absence_type):

    df = pd.read_csv(ABSENCE_FILE)

    employee_absences = df[
        (df["employee_id"] == employee_id)
        & (df["absence_type"] == absence_type)
    ]

    hours_used = employee_absences["hours_missed"].sum()

    DEFAULT_ALLOWANCES = {
        "sick_leave": 80,      # 10 days
        "bereavement": 24,     # 3 days
        "vacation": 120,       # example
        "pto": 120
    }

    allowance = DEFAULT_ALLOWANCES.get(absence_type, 0)

    return {
        "absence_type": absence_type,
        "hours_used": float(hours_used),
        "hours_remaining": max(
            allowance - float(hours_used),
            0
        )
    }
  
import os
from datetime import datetime

if os.path.exists("absences.csv"):
    df = pd.read_csv("absences.csv")
else:
    df = pd.DataFrame(columns=["employee_id", "date", "absence_type", "hours_missed", "region", "employment_type"])

def record_absence(employee_id, date, abs_type, hrs_missed, region, emp_type):
    global df
    new_absence = {
        "employee_id": employee_id,
        "date": date,
        "absence_type": abs_type,
        "hours_missed": hrs_missed,
        "region": region,
        "employment_type":emp_type
    }
    new_row = pd.DataFrame([new_absence])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("absences.csv", index=False)

def get_absence_by_employee(employee_id):
    return df[df["employee_id"] == employee_id].to_dict(orient="records")

def get_absence_by_month(month, year):
    all_absences = get_all_absences()
    monthly_abs_list = []
    for record in all_absences:
        try:
            date = datetime.strptime(record["date"], "%Y-%m-%d")
            if (date.month == month) and (date.year == year):
                monthly_abs_list.append(record)
        except ValueError:
            continue
    return monthly_abs_list
        
def get_all_absences():
    return df.to_dict(orient="records")

def update_absence(employee_id, field, new_value):
    global df
    
    # check if employee exists first
    if not (df["employee_id"] == employee_id).any():
        return f"Employee {employee_id} not found"
    
    # update the specific field
    df.loc[df["employee_id"] == employee_id, field] = new_value
    
    # save back to CSV
    df.to_csv("absences.csv", index=False)
    
    return f"Updated {field} to {new_value} for {employee_id}"

def delete_absence(emp_id, date, abs_type):
    global df
    if not ((df["employee_id"] == emp_id) & (df["date"] == date) & (df["absence_type"] == abs_type)).any():
        return f"Employee {emp_id}'s absence of {abs_type} on {date} not found"
    df = df[~((df["employee_id"] == emp_id) & (df["date"] == date) & (df["absence_type"] == abs_type))]

    # save back to CSV
    df.to_csv("absences.csv", index=False)
    
    return f"Deleted {emp_id}'s absence of {abs_type} on {date} from database"

def get_used_paid_days(employee_id, absence_type):
    absences = get_absence_by_employee(employee_id)
    count = sum(1 for a in absences if a["absence_type"] == absence_type)
    return count

import pandas as pd
import os
from datetime import datetime

if os.path.exists("hours_log.csv"):
    df = pd.read_csv("hours_log.csv")
else:
    df = pd.DataFrame(columns=["employee_id", "week_start_date", "hours_worked", "employment_type"])

def record_hours(employee_id, date, hrs_worked, emp_type):
    global df
    new_hours = {
        "employee_id": employee_id,
        "week_start_date": date,
        "hours_worked": hrs_worked,
        "employment_type":emp_type
    }
    new_row = pd.DataFrame([new_hours])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("absences.csv", index=False)

def get_hours_by_employee(employee_id):
    return df[df["employee_id"] == employee_id].to_dict(orient="records")

def get_monthly_hours(employee_id, month, year):
    employee_hours = get_hours_by_employee(employee_id)
    total = 0
    for record in employee_hours:
        try:
            week_date = datetime.strptime(record["week_start_date"], "%Y-%m-%d")
            if week_date.month == month and week_date.year == year:
                total += float(record["hours_worked"])
        except ValueError:
            continue
    return total

def get_weekly_hours(employee_id, week_start_date):
    matching = df[(df["employee_id"] == employee_id) & (df["week_start_date"] == week_start_date)]
    if matching.empty:
        return None
    return matching.iloc[0]["hours_worked"]
        
def update_hours(employee_id, week_start_date, new_hours):
    global df
    if not ((df["employee_id"] == employee_id) & (df["week_start_date"] == week_start_date)).any():
        return f"No record found for {employee_id} on {week_start_date}"
    df.loc[(df["employee_id"] == employee_id) & (df["week_start_date"] == week_start_date), "hours_worked"] = new_hours
    df.to_csv("hours_worked.csv", index=False)
    return f"Updated hours to {new_hours} for {employee_id} on {week_start_date}"

def delete_hours(employee_id, week_start_date):
    global df
    if not ((df["employee_id"] == employee_id) & (df["week_start_date"] == week_start_date)).any():
        return f"No record found for {employee_id} on {week_start_date}"
    df = df[~((df["employee_id"] == employee_id) & (df["week_start_date"] == week_start_date))]
    df.to_csv("hours_worked.csv", index=False)
    return f"Deleted hours record for {employee_id} on {week_start_date}"

def get_average_weekly_hours(employee_id, month, year):
    total_hours = get_monthly_hours(employee_id, month, year)
    employee_hours = get_hours_by_employee(employee_id)
    weeks_in_month = sum(
        1 for r in employee_hours 
        if datetime.strptime(r["week_start_date"], "%Y-%m-%d").month == month
        and datetime.strptime(r["week_start_date"], "%Y-%m-%d").year == year
    )
    if weeks_in_month == 0:
        return 0
    return total_hours / weeks_in_month
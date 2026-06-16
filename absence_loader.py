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
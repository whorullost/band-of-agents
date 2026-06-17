from agent2_security import run_security_check
from agent1_onboarding import ag1_get_employee_field_by_anon
from absence_loader import record_absence, get_used_paid_days, delete_absence, update_absence, get_all_absences, get_absence_by_month, get_absence_by_employee, get_absence_by_field
from deduction_ai import get_deduction_rules
from datetime import datetime

#TODO: update security actions after syncing with Iris on access_control.py

EXCESSIVE_ABSENCE_THRESHOLD = 40  # hours/month

def ag3_record_absence(user, employee_id, date, abs_type, hrs_missed, region, emp_type):
    if run_security_check(user, "record_absence"):
        record_absence(employee_id, date, abs_type, hrs_missed, region, emp_type)
        return f"Absence for {employee_id} recorded successfully"
    else:
        return "Invalid action"

def ag3_get_used_paid_days(user, employee_id, absence_type):
    if run_security_check(user, "record_absence"):
        return get_used_paid_days(employee_id, absence_type)
    else:
        return "Invalid action"

def ag3_delete_absence(user, emp_id, date, abs_type):
    if run_security_check(user, "record_absence"):
        return delete_absence(emp_id, date, abs_type)
    else:
        return "Invalid action"

def ag3_update_absence(user, employee_id, field, new_value):
    if run_security_check(user, "record_absence"):
        return update_absence(employee_id, field, new_value)
    else:
        return "Invalid action"
    
def ag3_get_all_absences(user):
    if run_security_check(user, "record_absence"):
        return get_all_absences()
    else:
        return "Invalid action"
    
def ag3_get_absence_by_month(user, month, year):
    if run_security_check(user, "record_absence"):
        return get_absence_by_month(month, year)
    else:
        return "Invalid action"
    
def ag3_get_absence_by_employee(user, employee_id):
    if run_security_check(user, "record_absence"):
        return get_absence_by_employee(employee_id)
    else:
        return "Invalid action"

def get_absence_field(user, employee_id, field):
    if run_security_check(user, "record_absence"):
        return get_absence_by_field(employee_id, field)
    else:
        return "Invalid action"
    
def flag_for_hr_review(employee_id, absence_type):
    return (f"{absence_type} for {employee_id} requires HR review")
    
def ag3_calculate_deduction(user, employee_id, month, year):
    if run_security_check(user, "record_absence"):
        absence_type = get_absence_field(user, employee_id, "absence_type")
        region = ag1_get_employee_field_by_anon(user, employee_id, "region")
        employment_type = ag1_get_employee_field_by_anon(user, employee_id, "employment_type")
        if (absence_type != "Access denied") and (region != "Invalid action") and (employment_type != "Invalid action"):
            deduction_result = get_deduction_rules(absence_type, region, employment_type)
        else:
            return "Invalid inputs"

        if deduction_result["requires_hr_review"]:
            return flag_for_hr_review(employee_id, absence_type)
        
        if ag3_get_used_paid_days(user, employee_id, absence_type) <= deduction_result["paid_days_allowed"]:
            return 0
        
        absences = get_absence_by_month(month, year)
        employee_absences = [
            a for a in absences
            if a["employee_id"] == employee_id
            and a["absence_type"] == absence_type
        ]

        base_salary = ag1_get_employee_field_by_anon(user, employee_id, "base_salary")
        deduction = 0

        if deduction_result["deduction_type"] == "full_day":
            days_missed = len(employee_absences)
            daily_rate = base_salary / 260
            deduction = daily_rate * days_missed
        elif deduction_result["deduction_type"] == "hourly":
            hours_missed = sum(a["hours_missed"] for a in employee_absences)
            hourly_rate = base_salary / 2080
            deduction = hourly_rate * hours_missed
        elif deduction_result["deduction_type"] == "none":
            deduction = 0
    
        return deduction
    return "Invalid action"

def ag3_flag_excessive_absences(user, employee_id, month, year):
    if run_security_check(user, "view_payroll"):
        absences = get_absence_by_employee(employee_id)
        monthly = [
            a for a in absences
            if datetime.strptime(a["date"], "%Y-%m-%d").month == month
        ]
        # change from len(monthly) >= 3 to hours-based
        total_hours = sum(float(a["hours_missed"]) for a in monthly)
        if total_hours >= EXCESSIVE_ABSENCE_THRESHOLD:
            print(f"{employee_id} has {total_hours} hours absent this month")
            return True
        return False
    return "Invalid action"

def ag3_get_absence_report(user, employee_id, month, year):
    if run_security_check(user, "record_absence"):
        absences = get_absence_by_employee(employee_id)
        monthly = [
            a for a in absences
            if datetime.strptime(a["date"], "%Y-%m-%d").month == month
            and datetime.strptime(a["date"], "%Y-%m-%d").year == year
        ]
        return {
            "employee_id": employee_id,
            "month": month,
            "year": year,
            "absence_count": len(monthly),
            "absences": monthly
        }
    return "Invalid action"
"""
if __name__ == "__main__":
    from absence_loader import record_absence
    
    # add test absences first
    record_absence("S_91550FEB", "2026-06-01", "sick_leave", 8, "California", "Full-Time")
    record_absence("S_91550FEB", "2026-06-03", "sick_leave", 8, "California", "Full-Time")
    record_absence("S_91550FEB", "2026-06-05", "unpaid_leave", 8, "California", "Full-Time")
    
    # test each function
    print("=== Testing Agent 3 ===")
    
    print("\n1. Get absence by employee:")
    print(ag3_get_absence_by_employee("anna.smith", "S_91550FEB"))
    
    print("\n2. Get used paid days:")
    print(ag3_get_used_paid_days("anna.smith", "S_91550FEB", "sick_leave"))
    
    print("\n3. Calculate deduction:")
    print(ag3_calculate_deduction("anna.smith", "S_91550FEB", 6, 2026))
    
    print("\n4. Flag excessive absences:")
    print(ag3_flag_excessive_absences("anna.smith", "S_91550FEB", 6, 2026))
    
    print("\n5. Get absence report:")
    print(ag3_get_absence_report("anna.smith", "S_91550FEB", 6, 2026))
"""

# ── IRIS'S VERSION (keeping for reference) ──────────────────
"""
# Agent 3: Absence management: recording absences, calculating deductions, leave balance, excessive absence flagging, absence reports

from absence_loader import (
    record_absence,
    get_absences_by_employee,
    get_leave_balance
)

from deduction_ai import get_deduction_rules

from access_control import authorize
from security_monitor import log_attempt

# Agent 1 interfaces (idk what is supposed to be here ig, maybe its supposed to be calling the data)
from employee_agent import (
    get_employee_salary,
    get_employee_region,
    get_employee_employment_type
)


EXCESSIVE_ABSENCE_THRESHOLD = 40  # hours/month


def _security_check(user, action):

    allowed = authorize(user, action)

    log_attempt(
        user=user,
        action=action,
        success=allowed
    )

    if not allowed:
        raise PermissionError(
            f"Unauthorized: {action}"
        )


def ag3_record_absence(
    user,
    employee_id,
    date,
    absence_type,
    hours_missed
):

    _security_check(user, "record_absence")

    region = get_employee_region(employee_id)
    employment_type = get_employee_employment_type(
        employee_id
    )

    record_absence(
        employee_id,
        date,
        absence_type,
        hours_missed,
        region,
        employment_type
    )

    flagged = ag3_flag_excessive_absences(
        user,
        employee_id
    )

    return {
        "success": True,
        "flagged": flagged
    }


def ag3_calculate_deduction(
    user,
    employee_id,
    month,
    year
):

    _security_check(
        user,
        "calculate_deduction"
    )

    absences = get_absences_by_employee(
        employee_id
    )

    salary = get_employee_salary(
        employee_id
    )

    region = get_employee_region(
        employee_id
    )

    employment_type = (
        get_employee_employment_type(
            employee_id
        )
    )

    daily_rate = salary / 260
    hourly_rate = daily_rate / 8

    total_deduction = 0

    for absence in absences:

        date_parts = absence["date"].split("-")

        if (
            int(date_parts[0]) != year
            or int(date_parts[1]) != month
        ):
            continue

        absence_type = absence["absence_type"]

        rules = get_deduction_rules(
            absence_type,
            region,
            employment_type
        )

        hours = float(
            absence["hours_missed"]
        )

        days = hours / 8

        if rules.get("always_deduct"):
            total_deduction += (
                daily_rate * days
            )

        elif rules.get("hourly_deduction"):
            total_deduction += (
                hourly_rate * hours
            )

    return round(total_deduction, 2)


def ag3_get_leave_balance(
    user,
    employee_id,
    absence_type
):

    _security_check(
        user,
        "view_leave_balance"
    )

    return get_leave_balance(
        employee_id,
        absence_type
    )


def ag3_flag_excessive_absences(
    user,
    employee_id
):

    _security_check(
        user,
        "flag_absences"
    )

    absences = get_absences_by_employee(
        employee_id
    )

    total_hours = sum(
        float(row["hours_missed"])
        for row in absences
    )

    return (
        total_hours >=
        EXCESSIVE_ABSENCE_THRESHOLD
    )


def ag3_get_absence_report(
    user,
    employee_id,
    month,
    year
):

    _security_check(
        user,
        "absence_report"
    )

    absences = get_absences_by_employee(
        employee_id
    )

    report = []

    for absence in absences:

        y, m, _ = absence["date"].split("-")

        if int(y) == year and int(m) == month:
            report.append(absence)

    return {
        "employee_id": employee_id,
        "month": month,
        "year": year,
        "absence_count": len(report),
        "absences": report
    }"""
# ── END IRIS'S VERSION ───────────────────────────────────────
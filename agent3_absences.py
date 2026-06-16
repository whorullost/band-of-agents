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
    }
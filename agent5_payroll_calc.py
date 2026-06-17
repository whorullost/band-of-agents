from agent2_security import run_security_check
from agent1_onboarding import ag1_get_employee_field_by_anon
from agent3_absence import ag3_calculate_deduction
from agent4_benefits import ag4_get_monthly_benefits_deduction
from hours_loader import get_monthly_hours, get_hours_by_employee

OVERTIME_THRESHOLD_PER_WEEK = 40
OVERTIME_MULTIPLIER = 1.5

def ag5_calculate_overtime(user, anon_id, month, year):
    if not run_security_check(user, "view_payroll"):
        return "Access denied"

    employment_type = ag1_get_employee_field_by_anon(user, anon_id, "employment_type")
    if employment_type != "Full-Time":
        return 0  # part-time employees don't get overtime in this system

    salary = ag1_get_employee_field_by_anon(user, anon_id, "base_salary")
    hourly_rate = salary / 2080  # 2080 = standard working hours/year

    weekly_records = get_hours_by_employee(anon_id)
    total_overtime_pay = 0

    for record in weekly_records:
        hours = float(record["hours_worked"])
        if hours > OVERTIME_THRESHOLD_PER_WEEK:
            overtime_hours = hours - OVERTIME_THRESHOLD_PER_WEEK
            total_overtime_pay += hourly_rate * OVERTIME_MULTIPLIER * overtime_hours

    return round(total_overtime_pay, 2)

def ag5_calculate_pay(user, anon_id, month, year):
    if not run_security_check(user, "view_payroll"):
        return "Access denied"

    salary = ag1_get_employee_field_by_anon(user, anon_id, "base_salary")
    monthly_base_pay = salary / 12

    overtime_pay = ag5_calculate_overtime(user, anon_id, month, year)

    absence_deduction = ag3_calculate_deduction(user, anon_id, month, year)
    if not isinstance(absence_deduction, (int, float)):
        absence_deduction = 0  # handles HR review flags or errors gracefully

    benefits_deduction = ag4_get_monthly_benefits_deduction(user, anon_id, month, year)
    if not isinstance(benefits_deduction, (int, float)):
        benefits_deduction = 0

    gross_pay = monthly_base_pay + overtime_pay
    total_deductions = absence_deduction + benefits_deduction
    net_pay = gross_pay - total_deductions

    return {
        "employee_id": anon_id,
        "month": month,
        "year": year,
        "monthly_base_pay": round(monthly_base_pay, 2),
        "overtime_pay": round(overtime_pay, 2),
        "gross_pay": round(gross_pay, 2),
        "absence_deduction": round(absence_deduction, 2),
        "benefits_deduction": round(benefits_deduction, 2),
        "total_deductions": round(total_deductions, 2),
        "net_pay": round(net_pay, 2)
    }

def ag5_run_payroll_all(user, anon_id_list, month, year):
    if not run_security_check(user, "view_payroll"):
        return "Access denied"

    results = []
    for anon_id in anon_id_list:
        result = ag5_calculate_pay(user, anon_id, month, year)
        results.append(result)
    return results

if __name__ == "__main__":
    print("=== Testing Agent 5 ===")
    print("\n1. Calculate overtime:")
    print(ag5_calculate_overtime("anna.smith", "S_91550FEB", 6, 2026))
    
    print("\n2. Calculate full pay:")
    print(ag5_calculate_pay("anna.smith", "S_91550FEB", 6, 2026))
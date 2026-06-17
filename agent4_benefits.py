# Agent 4: Benefit agents: health insurance/retirement, stocks

from agent2_security import run_security_check
from agent1_onboarding import ag1_get_employee_field_by_anon
from hours_loader import get_average_weekly_hours
from benefit_calculator import calculate_health_benefit, calculate_retirement_match, calculate_stock_options, calculate_years_of_service


def ag4_calculate_benefits(user, anon_id, month, year):
    if not run_security_check(user, "view_payroll"):
        return "Access denied"

    employment_type = ag1_get_employee_field_by_anon(user, anon_id, "employment_type")
    yearly_salary = ag1_get_employee_field_by_anon(user, anon_id, "base_salary")
    salary = yearly_salary/12
    health_insurance = ag1_get_employee_field_by_anon(user, anon_id, "health_insurance")
    retirement_contribution = ag1_get_employee_field_by_anon(user, anon_id, "retirement_contribution")
    stock_option = ag1_get_employee_field_by_anon(user, anon_id, "stock_options")
    start_date = ag1_get_employee_field_by_anon(user, anon_id, "start_date")

    years = calculate_years_of_service(start_date)

    # FULL TIME
    if employment_type == "Full-Time":
        health_info = calculate_health_benefit(employment_type, health_insurance)
        retirement_info = calculate_retirement_match(salary, retirement_contribution, hours_per_week=40)
        stock_info = calculate_stock_options(stock_option, start_date, hours_per_week=40)

    # PART TIME — based on actual hours worked that month
    else:
        avg_hours_per_week = get_average_weekly_hours(anon_id, month, year)
        health_info = calculate_health_benefit(employment_type, health_insurance)  # not eligible if not Full-Time
        retirement_info = calculate_retirement_match(salary, retirement_contribution, avg_hours_per_week)
        stock_info = calculate_stock_options(stock_option, start_date, avg_hours_per_week)

    return {
        "employee_id": anon_id,
        "health_insurance": health_info,
        "retirement_match": retirement_info,
        "stock_options": stock_info,
        "years_of_service": years
    }

def ag4_get_monthly_benefits_deduction(user, anon_id, month, year):
    """Returns just the dollar amount to deduct from paycheck for benefits.
    (Health insurance + employee's own retirement contribution — 
    company match doesn't come out of employee's paycheck)
    """
    if not run_security_check(user, "view_payroll"):
        return "Access denied"

    benefits = ag4_calculate_benefits(user, anon_id, month, year)

    health_deduction = benefits["health_insurance"].get("monthly_company_cost", 0) if benefits["health_insurance"]["eligible"] else 0
    
    salary = ag1_get_employee_field_by_anon(user, anon_id, "base_salary")
    retirement_contribution = ag1_get_employee_field_by_anon(user, anon_id, "retirement_contribution")
    contribution_pct = float(str(retirement_contribution).replace("%", ""))
    monthly_salary = salary / 12
    employee_retirement_deduction = monthly_salary * (contribution_pct / 100)

    total_deduction = health_deduction + employee_retirement_deduction

    return round(total_deduction, 2)

"""
if __name__ == "__main__":
    # need a valid anon_id from your employee dataset
    # get one by running ag1_get_all_employees first, copy an employee_id from output
    
    test_anon_id = "S_91550FEB"  # replace with actual anon ID from your data
    
    print("=== Testing Agent 4 ===")
    print("\n1. Calculate full benefits:")
    print(ag4_calculate_benefits("anna.smith", test_anon_id, 6, 2026))
    
    print("\n2. Get monthly deduction amount:")
    print(ag4_get_monthly_benefits_deduction("anna.smith", test_anon_id, 6, 2026))
    """
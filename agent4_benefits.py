# Agent 4: Benefit agents: health insurance/retirement, stocks

from datetime import datetime
from benefits import calculate_health_benefit, calculate_retirement_match, calculate_stock_options, 

#FULL TIME HEALTH INSURANCE, RETIREMENT, STOCK
def calculate_years_of_service(start_date):
    start = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    )

    return (
        datetime.now() - start
    ).days // 365


def calculate_benefits(employee):

    salary = employee["base_salary"]

    years = calculate_years_of_service(
        employee["start_date"]
    )

    retirement_match = calculate_retirement_match(
        salary,
        employee["retirement_contribution"]
    )

    stock_info = calculate_stock_options({
        **employee,
        "years_of_service": years
    })

    return {
        "employee_id": employee["employee_id"],

        "health_insurance":
            calculate_health_benefit(employee),

        "retirement_match":
            retirement_match,

        "stock_options":
            stock_info,

        "years_of_service":
            years
    }

#PART TIME RETIREMENT & STOCK (based on hours)
benefits = {
    "retirement": calculate_retirement_match(
        employee["base_salary"],
        employee["retirement_contribution"],
        employee["hours_per_week"]
    ),

    "stock_options": calculate_stock_options(
        employee,
        employee["hours_per_week"],
        years_of_service
    )
}
# for agent 4
#is technically pulling from employee dataset so need to change to fit into w/ agent 1 and 2 framework, but can be used for reference for now
# no need to read in / anonymized: name, department, manager_id, hr_role, job_title

#HEALTH INSURANCE: full time eligible, part time not eligible, contract not eligible
#   FULL TIME HEALTH INSURANCE: Basic plan costs company $5000/year, Premium plan costs company $8000/year
def calculate_health_benefit(employee):
    if employee["employment_type"] != "Full-Time":
        return {
            "eligible": False,
            "company_cost": 0
        }

    plans = {
        "Basic": 5000,
        "Premium": 8000
    }

    plan = employee["health_insurance"]

    return {
        "eligible": True,
        "plan": plan,
        "annual_company_cost": plans.get(plan, 0)
    }

#RETIREMENT/401K CONTRIBUTION: full time eligible, part time pro-rated based on hours, contract not eligible
#   FULL TIME RETIREMENT: that 100% match up to 3% of salary, then 50% match for next 2% of salary, max 4% total match
def calculate_retirement_match(salary, contribution_pct):

    contribution_pct = float(
        str(contribution_pct).replace("%", "")
    )

    match_pct = min(contribution_pct, 3)

    if contribution_pct > 3:
        match_pct += min(
            contribution_pct - 3,
            2
        ) * 0.5

    company_match = salary * (match_pct / 100)

    return round(company_match, 2)

#   PART TIME RETIREMENT MATCH: 50% of full time match if working 20-30 hours, 0% if less than 20 hours
def calculate_retirement_match(
    salary,
    contribution_pct,
    hours_per_week
):

    contribution_pct = float(
        str(contribution_pct).replace("%", "")
    )

    # Standard company match:
    # 100% of first 3%
    # 50% of next 2%

    match_pct = min(contribution_pct, 3)

    if contribution_pct > 3:
        match_pct += min(
            contribution_pct - 3,
            2
        ) * 0.5

    # Adjust for part-time status
    if hours_per_week < 20:
        multiplier = 0

    elif hours_per_week < 30:
        multiplier = 0.5

    else:
        multiplier = 1.0

    company_match = (
        salary *
        (match_pct / 100) *
        multiplier
    )

    return {
        "eligible": multiplier > 0,
        "company_match": round(company_match, 2)
    }

#STOCK OPTIONS: full time eligible, part time pro-rated based on hours, contract not eligible
#   FULL TIME STOCK OPTIONS: 100% of options vest after 4 years, with linear vesting in between (25% after 1 year, 50% after 2 years, 75% after 3 years)
def calculate_stock_options(employee):

    if employee["stock_options"] != "Yes":
        return {
            "eligible": False
        }

    years = employee["years_of_service"]

    if years < 1:
        vested = 0

    elif years < 2:
        vested = 25

    elif years < 3:
        vested = 50

    elif years < 4:
        vested = 75

    else:
        vested = 100

    return {
        "eligible": True,
        "vested_percent": vested
    }

#   PART TIME STOCK OPTIONS: 50% of full time options if working 20-30 hours, 0% if less than 20 hours, with same vesting schedule as full time
def calculate_stock_options(
    employee,
    hours_per_week,
    years_of_service
):

    if employee["stock_options"] != "Yes":
        return {
            "eligible": False
        }

    if hours_per_week < 20:
        grant_multiplier = 0

    elif hours_per_week < 30:
        grant_multiplier = 0.5

    else:
        grant_multiplier = 1.0

    # Example base grant
    base_grant = 1000

    granted_shares = int(
        base_grant * grant_multiplier
    )

    # Vesting schedule
    if years_of_service < 1:
        vested_pct = 0

    elif years_of_service < 2:
        vested_pct = 25

    elif years_of_service < 3:
        vested_pct = 50

    elif years_of_service < 4:
        vested_pct = 75

    else:
        vested_pct = 100

    vested_shares = int(
        granted_shares *
        vested_pct / 100
    )

    return {
        "eligible": granted_shares > 0,
        "granted_shares": granted_shares,
        "vested_percent": vested_pct,
        "vested_shares": vested_shares
    }
import json

DEFAULT_RULES = {
    "sick_leave": {
        "paid_days": 5,
        "deduct_after_limit": True
    },
    "vacation": {
        "requires_balance": True
    },
    "pto": {
        "requires_balance": True
    },
    "unpaid_leave": {
        "always_deduct": True
    },
    "late": {
        "hourly_deduction": True
    },
    "no_show": {
        "always_deduct": True,
        "flag": True
    },
    "bereavement": {
        "paid_days": 3
    },
    "fmla": {
        "always_flag_hr": True,
        "deduction": False
    }
}


def get_deduction_rules(
    absence_type,
    region,
    employment_type
):
    """
    Placeholder for OpenAI/Claude/etc.

    ONLY SEND:
        absence_type
        region
        employment_type

    NEVER SEND:
        salary
        name
        employee_id
    """

    try:

        prompt = {
            "absence_type": absence_type,
            "region": region,
            "employment_type": employment_type
        }

        # AI call would go here

        ai_response = DEFAULT_RULES.get(
            absence_type,
            {}
        )

        if validate_rules(ai_response):
            return ai_response

    except Exception:
        pass

    return DEFAULT_RULES.get(absence_type, {})


def validate_rules(ai_response):

    if not isinstance(ai_response, dict):
        return False

    allowed_keys = {
        "paid_days",
        "deduct_after_limit",
        "always_deduct",
        "hourly_deduction",
        "flag",
        "requires_balance",
        "always_flag_hr",
        "deduction"
    }

    return all(
        key in allowed_keys
        for key in ai_response.keys()
    )
import requests
import os
import json

CACHE_FILE = "rules_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

rules_cache = load_cache()

DEFAULT_RULES = {
    "sick_leave": {
        "paid_days_allowed": 5,
        "deduction_type": "full_day",
        "requires_hr_review": False,
        "notes": "Default: 5 paid sick days per year"
    },
    "unpaid_leave": {
        "paid_days_allowed": 0,
        "deduction_type": "full_day",
        "requires_hr_review": False,
        "notes": "Always unpaid"
    },
    "late": {
        "paid_days_allowed": 0,
        "deduction_type": "hourly",
        "grace_period_minutes": 30,
        "requires_hr_review": False,
        "notes": "Deduct hourly rate after 30 min grace period"
    },
    "no_show": {
        "paid_days_allowed": 0,
        "deduction_type": "full_day",
        "requires_hr_review": True,
        "notes": "Always deduct, flag for HR review"
    },
    "vacation": {
        "paid_days_allowed": 10,
        "deduction_type": "full_day",
        "requires_hr_review": False,
        "notes": "Based on accrued PTO balance"
    },
    "bereavement": {
        "paid_days_allowed": 3,
        "deduction_type": "full_day",
        "requires_hr_review": False,
        "notes": "3 paid bereavement days"
    },
    "fmla": {
        "paid_days_allowed": 0,
        "deduction_type": "none",
        "requires_hr_review": True,
        "notes": "FMLA: up to 12 weeks, job protected, flag for HR"
    }
}

def get_default_rules():
    return DEFAULT_RULES

API_KEY = "Insert API Key"

def deduction_ai(absence_type, region, employment_type):
    prompt = f"""
    Given the following information:
    - Absence type: {absence_type}
    - Region/State: {region}
    - Employment type: {employment_type}

    Return ONLY a JSON object with these exact fields, no other text:
    {{
        "paid_days_allowed": <integer, how many paid days per year>,
        "deduction_type": <"full_day", "hourly", or "none">,
        "grace_period_minutes": <integer, only relevant if late, otherwise 0>,
        "requires_hr_review": <true or false>,
        "notes": "<brief explanation of the rule and its legal basis>"
    }}

    Base your response on current {region} labor laws.
    If unsure, use federal US law as default.
    """
    try:
        response = requests.post("https://",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gemini-2.0-flash",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a labor law expert specializing in payroll deductions"
                    },
                    {
                        "role":"user",
                        "content": prompt
                    }
                ]
            }
        )
        text = response.json()["choices"][0]["message"]["content"]
        rules = json.loads(text)
        return rules
    except Exception as e:
        print(f"AI failed {e}, use default rules")
        return None    
    
def validate_rules(rules):
    if rules is None:
        return False
    if not 0 <= rules.get("paid_days_allowed", -1) <= 365:
        return False
    if rules.get("deduction_type") not in ["full_day", "hourly", "none"]:
        return False
    if not isinstance(rules.get("requires_hr_review"), bool):
        return False
    return True

def get_deduction_rules(absence_type, region, employment_type):
    cache_key = f"{absence_type}_{region}_{employment_type}"
    if cache_key in rules_cache:
        print(f"Using cached rules for {cache_key}")
        return rules_cache[cache_key]
    
    # get AI rules
    ai_rules = deduction_ai(absence_type, region, employment_type)
    
    # validate
    if validate_rules(ai_rules):
        rules_cache[cache_key] = ai_rules
        save_cache(rules_cache)
        return ai_rules
    
    # fallback to defaults
    print(f"Using default rules for {absence_type}")
    return DEFAULT_RULES.get(absence_type, DEFAULT_RULES["unpaid_leave"])

"""  
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
    """

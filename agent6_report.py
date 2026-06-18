import requests
import json
from agent2_security import run_security_check
from agent5_payroll_calc import ag5_calculate_pay
from agent4_benefits import ag4_calculate_benefits
from agent3_absence import ag3_flag_excessive_absences

API_KEY = "Insert API Key"

def call_ai_for_explanation(payroll_data, benefits_data, excessive_flag):
    prompt = f"""
    You are an HR payroll assistant. Explain this employee's payroll report 
    in clear, professional, plain English for an HR manager to read.

    Payroll data:
    {json.dumps(payroll_data)}

    Benefits and stock data:
    {json.dumps(benefits_data)}

    Excessive absences this month: {excessive_flag}

    Write a short, clear summary (3-5 sentences) explaining:
    - Why the net pay is what it is
    - Any notable deductions
    - Stock vesting status
    - Whether anything needs HR attention

    Return ONLY the summary text, no preamble, no markdown.
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
                        "content": "You are a clear, concise HR payroll assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        )
        text = response.json()["choices"][0]["message"]["content"]
        return text
    except Exception as e:
        print(f"AI failed {e}, using basic template")
        return None

def generate_fallback_summary(payroll_data, benefits_data, excessive_flag):
    summary = (
        f"Net pay for this period is ${payroll_data['net_pay']}. "
        f"Total deductions were ${payroll_data['total_deductions']} "
        f"(absences: ${payroll_data['absence_deduction']}, benefits: ${payroll_data['benefits_deduction']}). "
    )
    if benefits_data.get("stock_options", {}).get("eligible"):
        vested = benefits_data["stock_options"]["vested_percent"]
        summary += f"Stock options are {vested}% vested. "
    if excessive_flag:
        summary += "This employee has excessive absences this month and may need HR review."
    return summary

def ag6_generate_report(user, anon_id, month, year):
    if not run_security_check(user, "view_payroll"):
        return "Access denied"

    payroll_data = ag5_calculate_pay(user, anon_id, month, year)
    benefits_data = ag4_calculate_benefits(user, anon_id, month, year)
    excessive_flag = ag3_flag_excessive_absences(user, anon_id, month, year)

    explanation = call_ai_for_explanation(payroll_data, benefits_data, excessive_flag)

    if not explanation:
        explanation = generate_fallback_summary(payroll_data, benefits_data, excessive_flag)

    return {
        "employee_id": anon_id,
        "month": month,
        "year": year,
        "payroll": payroll_data,
        "benefits": benefits_data,
        "excessive_absences": excessive_flag,
        "summary": explanation
    }

if __name__ == "__main__":
    print("=== Testing Agent 6 ===")
    print(ag6_generate_report("anna.smith", "S_91550FEB", 6, 2026))
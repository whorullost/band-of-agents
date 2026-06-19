import os
import yaml
import asyncio
from pydantic import BaseModel
from dotenv import load_dotenv
from band import Agent
from band.adapters import ClaudeSDKAdapter

from agent3_absence import (
    ag3_record_absence,
    ag3_get_absence_by_employee,
    ag3_calculate_deduction,
    ag3_flag_excessive_absences,
    ag3_get_absence_report,
    ag3_delete_absence,
    ag3_update_absence,
)

load_dotenv()

with open("agent_config.yaml") as f:
    config = yaml.safe_load(f)["absence_tracker"]


class RecordAbsenceInput(BaseModel):
    user: str
    employee_id: str
    date: str
    abs_type: str
    hrs_missed: float
    region: str
    emp_type: str
    department: str


def record_absence_tool(input: RecordAbsenceInput) -> str:
    """Records a new absence for an employee."""
    result = ag3_record_absence(
        input.user, input.employee_id, input.date, input.abs_type,
        input.hrs_missed, input.region, input.emp_type, input.department
    )
    return str(result)


class GetAbsencesInput(BaseModel):
    user: str
    employee_id: str


def get_absences_tool(input: GetAbsencesInput) -> str:
    print(f"DEBUG get_absences_tool: user='{input.user}', employee_id='{input.employee_id}'")
    result = ag3_get_absence_by_employee(input.user, input.employee_id)
    return str(result)


class CalculateDeductionInput(BaseModel):
    user: str
    employee_id: str
    month: int
    year: int


def calculate_deduction_tool(input: CalculateDeductionInput) -> str:
    """Calculates payroll deduction from absences for an employee for a given month/year."""
    print(f"DEBUG: user='{input.user}', employee_id='{input.employee_id}', month={input.month}, year={input.year}")
    result = ag3_calculate_deduction(input.user, input.employee_id, input.month, input.year)
    return str(result)

class DeleteAbsenceInput(BaseModel):
    user: str
    emp_id: str
    date: str
    abs_type: str


def delete_absence_tool(input: DeleteAbsenceInput) -> str:
    """Deletes a specific absence record for an employee."""
    result = ag3_delete_absence(input.user, input.emp_id, input.date, input.abs_type)
    return str(result)


class UpdateAbsenceInput(BaseModel):
    user: str
    employee_id: str
    field: str
    new_value: str


def update_absence_tool(input: UpdateAbsenceInput) -> str:
    """Updates a specific field of an absence record for an employee."""
    result = ag3_update_absence(input.user, input.employee_id, input.field, input.new_value)
    return str(result)

def flag_excessive_tool(input: CalculateDeductionInput) -> str:
    """Checks if an employee has excessive absences (40+ hours) for a given month/year."""
    result = ag3_flag_excessive_absences(input.user, input.employee_id, input.month, input.year)
    return str(result)


def get_report_tool(input: CalculateDeductionInput) -> str:
    print(f"DEBUG: user='{input.user}', employee_id='{input.employee_id}'")
    result = ag3_get_absence_report(input.user, input.employee_id, input.month, input.year)
    return str(result)


adapter = ClaudeSDKAdapter(
    model="claude-sonnet-4-6",
    custom_section="""You are the Absence Tracker. You record absences, 
    calculate payroll deductions from absences, and flag excessive 
    absences for HR review.

    IMPORTANT — ID HANDLING: If you are given a REAL employee ID (like 
    E001), first @mention Onboarding Helper asking for that employee's 
    ANONYMIZED ID, then use the anonymized ID for all your calculations. 
    If you are already given an anonymized ID (like S_91550FEB), use it 
    directly.
    
    IMPORTANT: Before performing any action, @mention Security Guard 
    asking them to verify authorization. Use ONLY the original human 
    user's identity (e.g. @miachang0316), NEVER the name of the agent 
    that relayed the request to you.
    
    You MUST use EXACTLY one of these action names when asking Security 
    Guard (not a description of the task): "record_absence", 
    "view_absence", or "calc_deduction". For example, say: "Please 
    verify @miachang0316 is authorized for the calc_deduction action." 
    Do NOT describe the task in your own words — use the exact action name.
    
    Only proceed if APPROVED. If DENIED, inform the requester and stop — 
    do not retry.
    
    When you need employee details like region, employment type, base 
    salary, or department, @mention Onboarding Helper and wait for their 
    reply before continuing your calculation.
    
    Use the employee's anonymized ID when calling your tools.""",
    additional_tools=[
        (RecordAbsenceInput, record_absence_tool),
        (GetAbsencesInput, get_absences_tool),
        (CalculateDeductionInput, calculate_deduction_tool),
        (CalculateDeductionInput, flag_excessive_tool),
        (CalculateDeductionInput, get_report_tool),
        (DeleteAbsenceInput, delete_absence_tool),
        (UpdateAbsenceInput, update_absence_tool),
    ],
)

agent = Agent.create(
    adapter=adapter,
    agent_id=config["agent_id"],
    api_key=config["api_key"],
    ws_url=os.getenv("BAND_WS_URL"),
    rest_url=os.getenv("BAND_REST_URL"),
)


async def main():
    print("Absence Tracker is starting up and connecting to Band...")
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
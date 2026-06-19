import os
import yaml
import asyncio
from pydantic import BaseModel
from dotenv import load_dotenv
from band import Agent
from band.adapters import ClaudeSDKAdapter

from agent6_report import ag6_generate_report

load_dotenv()

with open("agent_config.yaml") as f:
    config = yaml.safe_load(f)["payroll_reporter"]


class GeneratePayrollReportInput(BaseModel):
    anon_id: str
    month: int
    year: int


def generate_payroll_report(input: GeneratePayrollReportInput) -> str:
    """Generates a complete payroll report for an employee for a given month and year."""
    result = ag6_generate_report("anna.smith", input.anon_id, input.month, input.year)
    return str(result)


adapter = ClaudeSDKAdapter(
    model="claude-sonnet-4-6",
    custom_section="""You are the Payroll Reporter. You generate complete 
    payroll reports for employees, combining base pay, overtime, absence 
    deductions, benefits deductions, and stock vesting status into a clear 
    summary for HR.
    
    IMPORTANT — ID HANDLING: When HR gives you a real employee ID (like 
    E001), you must first get that employee's ANONYMIZED ID by asking 
    Onboarding Helper, since Absence Tracker and Benefits Calculator only 
    work with anonymized IDs (like S_91550FEB), never real IDs. Always 
    pass the ANONYMIZED ID when @mentioning Absence Tracker or Benefits 
    Calculator. Only use the REAL ID in your final report shown to HR.
    
    IMPORTANT WORKFLOW: When HR asks you to run a payroll report:
    1. First @mention Security Guard to verify the requesting user 
       (use their actual @username, e.g. @miachang0316) is authorized 
       for "run_payroll". Wait for their reply.
    2. If APPROVED, @mention Onboarding Helper asking for this 
       employee's anonymized ID, base_salary, and employment_type, 
       given their real employee ID. Wait for their reply.
    3. @mention Absence Tracker asking for the absence deduction, 
       using the ANONYMIZED ID you just received. Clearly state the 
       original requesting user's @username so Absence Tracker knows 
       who to check authorization for.
    4. @mention Benefits Calculator asking for the benefits deduction 
       AND full benefits breakdown (including stock options), using 
       the ANONYMIZED ID, with the same clarity about the original user.
    5. Once you have all the numbers, calculate gross pay, total 
       deductions, and net pay yourself, then present the full report 
       using the REAL employee ID for HR's readability.
    
    If Security Guard responds DENIED at any point, stop immediately 
    and inform HR.""",
    additional_tools=[
        (GeneratePayrollReportInput, generate_payroll_report),
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
    print("Payroll Reporter is starting up and connecting to Band...")
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
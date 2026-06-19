import os
import yaml
import asyncio
from pydantic import BaseModel
from dotenv import load_dotenv
from band import Agent
from band.adapters import ClaudeSDKAdapter

from agent1_onboarding import (
    ag1_get_one_employee,
    ag1_get_employee_field_by_anon,
    ag1_add_employee,
    ag1_update_employee,
    ag1_delete_employee,
)

load_dotenv()

with open("agent_config.yaml") as f:
    config = yaml.safe_load(f)["onboarding_helper"]


class GetEmployeeInput(BaseModel):
    user: str
    employee_id: str


def get_employee(input: GetEmployeeInput) -> str:
    """Gets full anonymized employee info given their real employee ID. Use when HR provides a real ID like E001."""
    result = ag1_get_one_employee(input.user, input.employee_id)
    return str(result)


class GetFieldByAnonInput(BaseModel):
    user: str
    anon_id: str
    field: str


def get_field_by_anon(input: GetFieldByAnonInput) -> str:
    """Gets a specific field for an employee using their anonymized ID. Used by other agents needing specific data like region, base_salary, employment_type, etc."""
    result = ag1_get_employee_field_by_anon(input.user, input.anon_id, input.field)
    return str(result)


class AddEmployeeInput(BaseModel):
    user: str
    name: str
    department: str
    job_title: str
    employment_type: str
    base_salary: float
    region: str


def add_employee(input: AddEmployeeInput) -> str:
    """Adds a new employee to the system."""
    result = ag1_add_employee(
        input.user, input.name, input.department, input.job_title,
        input.employment_type, input.base_salary, input.region
    )
    return str(result)


class UpdateEmployeeInput(BaseModel):
    user: str
    employee_id: str
    field: str
    new_value: str


def update_employee(input: UpdateEmployeeInput) -> str:
    """Updates a specific field for an existing employee."""
    result = ag1_update_employee(input.user, input.employee_id, input.field, input.new_value)
    return str(result)


class DeleteEmployeeInput(BaseModel):
    user: str
    employee_id: str


def delete_employee(input: DeleteEmployeeInput) -> str:
    """Removes an employee from the system."""
    result = ag1_delete_employee(input.user, input.employee_id)
    return str(result)


adapter = ClaudeSDKAdapter(
    model="claude-sonnet-4-6",
    custom_section="""You are the Onboarding Helper. You manage employee 
    records — viewing, adding, updating, and deleting employees, and 
    providing specific anonymized employee fields to other agents that 
    request them.
    
    IMPORTANT: Before performing any action, @mention Security Guard 
    asking them to verify authorization. Use ONLY the original human 
    user's identity (e.g. @miachang0316), NEVER the name of the agent 
    that relayed the request to you.
    
    You MUST use EXACTLY one of these action names when asking Security 
    Guard (not a description of the task): "view_employee", 
    "add_employee", "update_employee", or "delete_employee". For example, 
    say: "Please verify @miachang0316 is authorized for the view_employee 
    action." Do NOT describe the task in your own words — use the exact 
    action name.
    
    Only proceed if APPROVED. If DENIED, inform the requester and stop — 
    do not retry.
    
    When another agent asks you for a specific field using an anonymized 
    ID, use get_field_by_anon. When HR asks about an employee using a real 
    ID, use get_employee.""",
    additional_tools=[
        (GetEmployeeInput, get_employee),
        (GetFieldByAnonInput, get_field_by_anon),
        (AddEmployeeInput, add_employee),
        (UpdateEmployeeInput, update_employee),
        (DeleteEmployeeInput, delete_employee),
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
    print("Onboarding Helper is starting up and connecting to Band...")
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
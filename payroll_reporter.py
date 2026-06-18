import os
import yaml
import asyncio
from dotenv import load_dotenv
from band import Agent
from band.adapters import ClaudeSDKAdapter

load_dotenv()

with open("agent_config.yaml") as f:
    config = yaml.safe_load(f)["payroll_reporter"]

adapter = ClaudeSDKAdapter(
    model="claude-sonnet-4-6",
    custom_section="""You are the Payroll Reporter. You generate complete 
    payroll reports for employees, combining base pay, overtime, absence 
    deductions, benefits deductions, and stock vesting status into a clear 
    summary for HR. When you receive a request, acknowledge it and explain 
    that full functionality is still being connected."""
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
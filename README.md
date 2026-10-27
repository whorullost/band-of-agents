# Secure Payroll Calculator

A multi-agent AI system with 6 specialized agents, including Onboarding, Security, Absences, Benefits, Payroll calculator, and Payroll Reporter, allowing for employees of a small to medium sized company to request information about payroll. There is anonymization of personal data with permission gateway, determining which AI's or users are allowed to access certain data. Returns paycheck reports with explanations and absence and benefit tracking. Using Band as a system to have agents communicate with each other in the chat room, allowing for any agent to being HR's entry point after being verified.


Built for **Lablab.ai's Band of Agents Hackathon** by Team [INSERT NAME HERE] ([whorullost](https://github.com/whorullost) & [tropilemon](https://github.com/tropilemon)).

## Problem
- Payroll is repetitive, tedious, and manual
- Existing tools calculate but don't explain
- Employees get treated as line items, not people
- Using AI on payroll data risks exposing sensitive information

## Solution
Six specialized agents coordinate through [Band](https://band.ai) to answer payroll questions, with three goals:
1. **Privacy:** personal data is anonymized before any AI sees it, behind a permission gateway
2. **Accuracy:** all math is deterministic; AI only explains
3. **Transparency:** every paycheck report comes with a plain-language explanation

## The agents
| # | Agent | What it does |
|---|---|---|
| 1 | **Onboarding Helper** | Keeps and passes along employee records. The only agent that ever touches raw, identifiable data; every other agent receives anonymized data through it. |
| 2 | **Security Guard** | The system's gatekeeper. Verifies the user's role and permissions before any action, checks for flagged accounts, and logs every decision. |
| 3 | **Absence Tracker** | Tracks absences and what they mean for a paycheck. Uses AI to apply region-specific labor law, determines leave types, calculates deductions, and flags excessive absences. |
| 4 | **Benefits Calculator** | Calculates health insurance costs, retirement matching, and stock option vesting based on employee status. Managers can view their team's benefits; only HR can calculate deductions. |
| 5 | **Payroll Calculator** (internal) | The math engine. Pure logic with no AI, so paycheck calculations are always precise and consistent. Runs inside the Payroll Reporter. |
| 6 | **Payroll Reporter** | Coordinates the other agents in real time and combines their results with an AI-generated explanation into one readable report. |

## How Band is used
- Agents communicate through @mentions in a shared Band chat
- The Payroll Reporter coordinates the full workflow
- Each agent independently verifies authorization before acting
- No single point of failure: once verified, any agent can serve as HR's entry point

## Responsible AI design
- AI never makes final payroll decisions
- Math stays deterministic; AI only explains
- Personal data is anonymized before AI ever sees it
- Every action is logged and auditable
- Designed so a buggy or compromised agent can't exceed its scope (see Limitations for what is implemented)

## Tech stack
- **Python:** core business logic for all agents
- **Band SDK + Claude adapter:** orchestration and @mention routing
- **AI/ML API:** labor law lookups and natural-language report generation
- **pandas:** data storage and management (CSV-based)
- **SHA-256 hashing:** deterministic anonymization of employee identifiers

## Limitations
- Hardcoded test users; there is no real login system yet
- Manager restrictions were tested directly, not shown live through Band
- Agent-level permissions (Layer 2) are designed but not fully wired in
- Monthly payroll only; no bi-weekly or weekly support
- Stock grants are flat, not role- or salary-based
- AI labor law guidance is assistive, not legal advice
- Hashing-based anonymization is pseudonymization, not full anonymization
- All data is [synthetic]; not for production payroll use

## Future improvements
- 2FA or password verification that the requester is the actual employee
- Compensation calculations beyond net salary
- Leave processing under FMLA
- Secure long-term payroll record keeping

## Team
For Lablab.ai's Band of Agents Hackathon
By Team [INSERT NAME HERE]! 

Members:
- [whorullost](https://github.com/whorullost)
- [tropilemon](https://github.com/tropilemon)



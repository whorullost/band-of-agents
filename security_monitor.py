# agent 1: security monitoring for access control

from datetime import datetime
import json

SECURITY_LOG = "security_events.jsonl"

#successful attempt to access payroll data
def log_attempt(username, action, success=False):

    event = {
        "timestamp": datetime.now().isoformat(),
        "username": username,
        "action": action,
        "success": success
    }

    with open(SECURITY_LOG, "a") as f:
        f.write(json.dumps(event) + "\n")

#failed attempt to access payroll data + flagging user for suspicious activity
def flag_user(username, reason, risk_score):

    event = {
        "timestamp": datetime.now().isoformat(),
        "username": username,
        "reason": reason,
        "risk_score": risk_score,
        "status": "FLAGGED"
    }

    with open(SECURITY_LOG, "a") as f:
        f.write(json.dumps(event) + "\n")    
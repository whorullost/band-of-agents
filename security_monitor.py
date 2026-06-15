# agent 1: security monitoring for access control

from datetime import datetime
from security_monitor import log_attempt, record_failure

audit_log = []

def log_attempt(user, action, allowed):
    audit_log.append({
        "timestamp": datetime.now(),
        "user": user,
        "action": action,
        "allowed": allowed
    })

failed_attempts = {}

def record_failure(user):
    failed_attempts[user] = (
        failed_attempts.get(user, 0) + 1
    )

    if failed_attempts[user] >= 3:
        return True

    return False

if record_failure(user):
    #need to have lockout mechanism + alert/record of sus activity (ex: multiple failed attempts)
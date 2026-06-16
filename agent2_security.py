#ToDo: Replace with actual code later, return true for agent1 checking purposes
from security_monitor import log_attempt, record_failure
from authorize import authorize

def run_security_check(user, action):
    if not authorize(user, action):
        log_attempt(user, action, allowed=False)
        record_failure(user)
        return False
    log_attempt(user, action, allowed=True)
    return True
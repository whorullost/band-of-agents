"""Logs all access attempts and tracks suspicious activity.
Part of Agent 2's security layer.
Records every action taken in the system for audit and compliance purposes.
Never import this directly into any AI agent"""

import pandas as pd
import os
from datetime import datetime

#Mia's
if os.path.exists("audit_log.csv"):
    df_login = pd.read_csv("audit_log.csv")
else:
    df_login = pd.DataFrame(columns=["timestamp", "user", "action", "allowed", "flagged"])

if os.path.exists("flagged_users.csv"):
    df_flagged = pd.read_csv("flagged_users.csv")
else:
    df_flagged = pd.DataFrame(columns=["user", "failed_attempts", "flagged", "timestamp_flagged"])

def is_flagged(user):
    matching = df_flagged[df_flagged["user"]==user]
    if matching.empty:
        return False
    return matching.iloc[0]["flagged"] == True

def log_attempt(user, action, allowed):
    global df_login
    new_attempt = {
        "timestamp": datetime.now(),
        "user": user,
        "action": action,
        "allowed": allowed,
        "flagged": is_flagged(user)
    }
    new_row = pd.DataFrame([new_attempt])
    df_login = pd.concat([df_login, new_row], ignore_index=True)
    df_login.to_csv("audit_log.csv", index=False)

failed_attempts = {}

def record_failure(user):
    global df_flagged
    failed_attempts[user] = (
        failed_attempts.get(user, 0) + 1
    )

    #failed attempt to access payroll data >= 5 + flagging user for suspicious activity
    if failed_attempts[user] >= 5:
        new_flag  = {
            "user":user,
            "failed_attempts":failed_attempts[user],
            "flagged":True,
            "timestamp_flagged":datetime.now()
        }
        new_row = pd.DataFrame([new_flag])
        df_flagged = pd.concat([df_flagged, new_row], ignore_index=True)
        df_flagged.to_csv("flagged_users.csv", index=False)
        print(f"SECURITY FLAG: {user} flagged for suspicious activity")
        return True
    return False

def get_audit_log():
     return df_login.to_dict(orient="records")


def unflag_user(user):
    global df_flagged
    df_flagged.loc[df_flagged["user"]== user, "flagged"] = False
    df_flagged.to_csv("flagged_users.csv", index=False)

def get_failed_attempts(user):
    if user in failed_attempts:
        return failed_attempts[user]
    else:
        return 0

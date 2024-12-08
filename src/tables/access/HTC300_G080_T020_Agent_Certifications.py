from ...imports import *

def convert_HTC300_G080_T020_Agent_Certifications(conn : Connection):
    agent_certificationInfo = conn.accessGetTableInfo('htc300', 'HTC300_G080_T020 Agent Certifications')
    for row in agent_certificationInfo:
        pass
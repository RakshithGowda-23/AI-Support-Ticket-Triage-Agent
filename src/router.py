ROUTING_MAP = {
    "Authentication": "Identity & Access Team",
    "Payment": "Payments Team",
    "Technical Issue": "Technical Support Team",
    "Account": "Account Management Team",
    "Service Outage": "Infrastructure Team",
    "Shipping": "Logistics Team",
    "General": "Customer Support Team"
}


def get_team(category: str) -> str:
    return ROUTING_MAP.get(category, "General Support Team")
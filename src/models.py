from pydantic import BaseModel, Field
from typing import Literal


class TicketAnalysis(BaseModel):
    category: Literal[
        "Authentication",
        "Payment",
        "Technical Issue",
        "Account",
        "Service Outage",
        "Shipping",
        "General"
    ]

    urgency: Literal[
        "Critical",
        "High",
        "Medium",
        "Low"
    ]

    confidence: float = Field(ge=0.0, le=1.0)

    route_to: str

    human_review: bool

    reason: str
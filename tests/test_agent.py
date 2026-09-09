from src.router import get_team
from src.models import TicketAnalysis


def test_payment_routes_to_payments_team():
    assert get_team("Payment") == "Payments Team"


def test_authentication_routes_to_identity_team():
    assert get_team("Authentication") == "Identity & Access Team"


def test_service_outage_routes_to_infrastructure_team():
    assert get_team("Service Outage") == "Infrastructure Team"


def test_shipping_routes_to_logistics_team():
    assert get_team("Shipping") == "Logistics Team"


def test_technical_issue_routes_to_technical_support():
    assert get_team("Technical Issue") == "Technical Support Team"


def test_account_routes_to_account_management():
    assert get_team("Account") == "Account Management Team"


def test_general_routes_to_customer_support():
    assert get_team("General") == "Customer Support Team"


def test_high_confidence_does_not_require_review():
    result = TicketAnalysis(
        category="Payment",
        urgency="High",
        confidence=0.95,
        route_to="Payments Team",
        human_review=False,
        reason="Payment failure"
    )

    assert result.confidence >= 0.70
    assert result.human_review is False


def test_low_confidence_requires_review():
    result = TicketAnalysis(
        category="General",
        urgency="Medium",
        confidence=0.55,
        route_to="Customer Support Team",
        human_review=True,
        reason="Ambiguous ticket"
    )

    assert result.confidence < 0.70
    assert result.human_review is True


def test_confidence_boundary():
    result = TicketAnalysis(
        category="Payment",
        urgency="Medium",
        confidence=0.70,
        route_to="Payments Team",
        human_review=False,
        reason="Clear payment issue"
    )

    assert result.confidence == 0.70
    assert result.human_review is False
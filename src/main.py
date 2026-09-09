import sys
import pandas as pd

from .agent import analyze_ticket


# Demo results are used only for offline testing.
# They do NOT call Gemini.
DEMO_RESULTS = {
    "T001": {
        "category": "Payment",
        "urgency": "High",
        "confidence": 0.95,
        "route_to": "Payments Team",
        "human_review": False,
        "reason": "The customer is experiencing a payment failure."
    },
    "T002": {
        "category": "Authentication",
        "urgency": "High",
        "confidence": 0.94,
        "route_to": "Identity & Access Team",
        "human_review": False,
        "reason": "The customer cannot log in to the account."
    },
    "T003": {
        "category": "Service Outage",
        "urgency": "Critical",
        "confidence": 0.96,
        "route_to": "Infrastructure Team",
        "human_review": False,
        "reason": "The website is completely unavailable."
    },
    "T004": {
        "category": "Account",
        "urgency": "Low",
        "confidence": 0.93,
        "route_to": "Account Management Team",
        "human_review": False,
        "reason": "The customer wants to change account information."
    },
    "T005": {
        "category": "Shipping",
        "urgency": "Medium",
        "confidence": 0.95,
        "route_to": "Logistics Team",
        "human_review": False,
        "reason": "The issue concerns a delayed package."
    },
    "T006": {
        "category": "Technical Issue",
        "urgency": "High",
        "confidence": 0.91,
        "route_to": "Technical Support Team",
        "human_review": False,
        "reason": "The application is crashing."
    },
    "T007": {
        "category": "Payment",
        "urgency": "Medium",
        "confidence": 0.90,
        "route_to": "Payments Team",
        "human_review": False,
        "reason": "The customer is asking about a refund."
    },
    "T008": {
        "category": "Authentication",
        "urgency": "High",
        "confidence": 0.92,
        "route_to": "Identity & Access Team",
        "human_review": False,
        "reason": "The password reset process is not working."
    },
    "T009": {
        "category": "Service Outage",
        "urgency": "Critical",
        "confidence": 0.97,
        "route_to": "Infrastructure Team",
        "human_review": False,
        "reason": "The production service is experiencing an outage."
    },
    "T010": {
        "category": "Shipping",
        "urgency": "Medium",
        "confidence": 0.94,
        "route_to": "Logistics Team",
        "human_review": False,
        "reason": "The customer needs help with a shipping address."
    },
    "T011": {
        "category": "Payment",
        "urgency": "Low",
        "confidence": 0.91,
        "route_to": "Payments Team",
        "human_review": False,
        "reason": "The customer is asking about available payment methods."
    },
    "T012": {
        "category": "Authentication",
        "urgency": "High",
        "confidence": 0.89,
        "route_to": "Identity & Access Team",
        "human_review": False,
        "reason": "The customer is unable to log in."
    },
    "T013": {
        "category": "Technical Issue",
        "urgency": "Medium",
        "confidence": 0.88,
        "route_to": "Technical Support Team",
        "human_review": False,
        "reason": "The dashboard is functioning slowly."
    },
    "T014": {
        "category": "Payment",
        "urgency": "High",
        "confidence": 0.96,
        "route_to": "Payments Team",
        "human_review": False,
        "reason": "The customer reports a duplicate payment charge."
    },
    "T015": {
        "category": "General",
        "urgency": "Medium",
        "confidence": 0.55,
        "route_to": "Customer Support Team",
        "human_review": True,
        "reason": "The ticket is ambiguous and does not clearly match a specific category."
    },
}


def process_tickets(input_file, output_file, demo=False):

    df = pd.read_csv(input_file)

    results = []

    print("\n======================================")
    print("     AI SUPPORT TICKET TRIAGE")
    print("======================================\n")

    if demo:
        print("MODE: OFFLINE DEMO")
        print("Gemini API will NOT be called.\n")
    else:
        print("MODE: GEMINI AI\n")

    print(f"Found {len(df)} tickets.\n")

    for _, row in df.iterrows():

        ticket_id = row["ticket_id"]

        print(f"Processing {ticket_id}...")

        try:

            if demo:

                if ticket_id not in DEMO_RESULTS:
                    raise ValueError(
                        f"No demo result available for {ticket_id}"
                    )

                result = DEMO_RESULTS[ticket_id]

                results.append({
                    "ticket_id": ticket_id,
                    "subject": row["subject"],
                    "category": result["category"],
                    "urgency": result["urgency"],
                    "confidence": result["confidence"],
                    "route_to": result["route_to"],
                    "human_review": result["human_review"],
                    "processing_status": "DEMO",
                    "reason": result["reason"]
                })

                print(
                    f"  ✓ {result['category']} | "
                    f"{result['urgency']} | "
                    f"{result['confidence']:.2f}"
                )

            else:

                result = analyze_ticket(
                    row["subject"],
                    row["message"]
                )

                results.append({
                    "ticket_id": ticket_id,
                    "subject": row["subject"],
                    "category": result.category,
                    "urgency": result.urgency,
                    "confidence": round(result.confidence, 2),
                    "route_to": result.route_to,
                    "human_review": result.human_review,
                    "processing_status": "CLASSIFIED",
                    "reason": result.reason
                })

                print(
                    f"  ✓ {result.category} | "
                    f"{result.urgency} | "
                    f"{result.confidence:.2f}"
                )

        except Exception as e:

            print(f"  ✗ Processing error: {e}")

            results.append({
                "ticket_id": ticket_id,
                "subject": row["subject"],
                "category": "",
                "urgency": "",
                "confidence": "",
                "route_to": "",
                "human_review": "",
                "processing_status": "API_ERROR",
                "reason": "Ticket could not be processed."
            })

    output_df = pd.DataFrame(results)

    output_df.to_csv(output_file, index=False)

    print("\n======================================")
    print("        PROCESSING COMPLETE")
    print("======================================")

    print(f"\nProcessed tickets : {len(results)}")
    print(f"Output file       : {output_file}")

    print("\nProcessing Status:")
    print(output_df["processing_status"].value_counts())

    print("\nCategories:")
    print(output_df["category"].value_counts())

    print("\nUrgency:")
    print(output_df["urgency"].value_counts())

    print("\nHuman Review:")
    print(output_df["human_review"].value_counts())


def main():

    demo = "--demo" in sys.argv

    process_tickets(
        "data/sample_tickets.csv",
        "outputs/triaged_tickets.csv",
        demo=demo
    )


if __name__ == "__main__":
    main()
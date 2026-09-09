import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from .models import TicketAnalysis
from .router import get_team
from .cache import get_cached_result, save_result


# Load environment variables from .env
load_dotenv()


# Create Gemini client
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. "
        "Please add your Gemini API key to the .env file."
    )


client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        timeout=120000
    )
)


SYSTEM_PROMPT = """
You are an AI Support Ticket Triage Agent.

Your job is to analyze customer support tickets and determine:

1. Category
2. Urgency
3. Confidence score
4. Appropriate support team
5. Whether human review is required
6. A short explanation for the decision

Allowed categories:
- Authentication
- Payment
- Technical Issue
- Account
- Service Outage
- Shipping
- General

Allowed urgency levels:
- Critical
- High
- Medium
- Low

Classification guidelines:

Authentication:
Problems with login, password, authentication, account access,
OTP, MFA, or inability to sign in.

Payment:
Payment failures, declined transactions, duplicate charges,
refunds, billing transactions, or payment methods.

Technical Issue:
Application bugs, crashes, errors, broken features, or technical
problems that are not a complete service outage.

Account:
Account information, profile changes, email changes, account
settings, or general account-management requests.

Service Outage:
Major service disruptions, website/platform completely unavailable,
production outages, or widespread service failures.

Shipping:
Delivery problems, delayed packages, shipping addresses,
tracking, or shipment-related issues.

General:
Requests that do not clearly fit another category.

Urgency guidelines:

Critical:
Complete service outage, major production failure, security-related
emergency, or issue affecting a large number of users.

High:
Important functionality is blocked, payment problems are preventing
an important transaction, or the customer needs urgent assistance.

Medium:
Normal support issue that affects the customer but is not immediately
business-critical.

Low:
General questions, information requests, minor issues, or non-urgent
requests.

Confidence:
Return a value between 0.0 and 1.0.

Use high confidence when the ticket clearly matches one category.
Use lower confidence when the ticket is ambiguous or could reasonably
belong to multiple categories.

The support team will be determined by the application based on the
category, so focus on correctly identifying the category.

Do not invent information that is not present in the ticket.
"""


def analyze_ticket(subject: str, message: str) -> TicketAnalysis:
    """
    Analyze a support ticket using Gemini.

    The function first checks the local cache. If the ticket has
    already been successfully analyzed, the cached result is returned
    without making another Gemini API request.

    If the ticket is not cached, Gemini analyzes it and the successful
    result is stored locally.
    """

    # ---------------------------------------------------------
    # 1. Check local cache first
    # ---------------------------------------------------------

    cached = get_cached_result(subject, message)

    if cached:
        print("  ✓ Using cached result")

        return TicketAnalysis(**cached)

    # ---------------------------------------------------------
    # 2. Prepare prompt
    # ---------------------------------------------------------

    prompt = f"""
{SYSTEM_PROMPT}

Customer Support Ticket

Subject:
{subject}

Message:
{message}

Analyze this ticket and return the required structured result.
"""

    # ---------------------------------------------------------
    # 3. Gemini request with limited retry handling
    # ---------------------------------------------------------

    max_retries = 4

    for attempt in range(max_retries):

        try:
            print(
                f"  Gemini attempt "
                f"{attempt + 1}/{max_retries}..."
            )

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=TicketAnalysis,
                ),
            )

            # -------------------------------------------------
            # 4. Validate Gemini response
            # -------------------------------------------------

            result = TicketAnalysis.model_validate_json(
                response.text
            )

            # -------------------------------------------------
            # 5. Determine routing using our application logic
            # -------------------------------------------------

            result.route_to = get_team(result.category)

            # Human review is determined by our decision boundary,
            # not by Gemini.
            result.human_review = result.confidence < 0.70

            # -------------------------------------------------
            # 6. Save successful result to cache
            # -------------------------------------------------

            save_result(
                subject,
                message,
                result
            )

            print("  ✓ Analysis successful")

            return result

        except Exception as e:
            error_text = str(e)

            # Handle Gemini timeout errors
            if (
                "504" in error_text
                or "DEADLINE_EXCEEDED" in error_text
            ):
                print("  Gemini request timed out.")

                if attempt < max_retries - 1:
                    delay = 5 * (2 ** attempt)

                    print(
                        f"  Retrying in {delay} seconds..."
                    )

                    time.sleep(delay)
                    continue

                raise

            # Handle Gemini temporary server errors
            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
            ):
                if attempt < max_retries - 1:
                    delay = 5 * (2 ** attempt)

                    print("  Gemini temporarily unavailable.")
                    print(f"  Retrying in {delay} seconds...")

                    time.sleep(delay)
                    continue

                raise

            # Handle quota/rate-limit errors
            if (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            ):
                print("  Gemini API quota/rate limit reached.")
                print("  No automatic retry will be performed.")
                raise

            raise
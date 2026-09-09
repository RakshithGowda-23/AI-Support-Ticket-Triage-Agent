Name: AI Support Ticket Triage Agent

Description:
An AI-powered support ticket triage system that analyzes incoming customer support tickets, classifies their category and urgency, assigns a confidence score, routes the ticket to the appropriate support team, and flags uncertain cases for human review.

The project uses Google Gemini 3.6 Flash for AI classification, Pydantic for structured validation, Pandas for CSV processing, a local JSON cache to avoid repeated API calls, and Streamlit for the web UI. It also has a CLI workflow and an offline demo mode.

CHALLENGE REQUIREMENTS:
The challenge requires:
- Public GitHub repository URL
- README with setup instructions, installation, API key configuration, and end-to-end run instructions
- Runnable agent
- Sample inputs and outputs
- Tradeoff notes explaining model/approach choices and improvements with more time
- Agent-specific deliverables

For the Support Ticket Triage Agent, the required capabilities are:
- Take a support ticket subject + body as input
- Classify each ticket by category and urgency with a confidence score
- Decide routing to the appropriate support team
- Flag uncertain cases for human review
- Process a batch of tickets and output routing decisions

Agent-specific deliverables:
- Sample support tickets
- Classified and routed output
- A note explaining the decision boundary

IMPORTANT:
A UI is optional in the challenge, but this project includes a Streamlit UI as an additional feature.

CURRENT PROJECT STRUCTURE:

AI-Support-Ticket-Triage-Agent/
├── src/
│   ├── __init__.py
│   ├── agent.py
│   ├── cache.py
│   ├── models.py
│   ├── router.py
│   └── main.py
├── data/
│   └── sample_tickets.csv
├── outputs/
│   └── triaged_tickets.csv
├── tests/
│   └── test_agent.py
├── app.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

IMPORTANT SECURITY NOTE:
The real .env file contains the Gemini API key and MUST NOT be committed to GitHub. The README must clearly instruct users to create their own .env file and must never show a real API key.

TECHNOLOGIES:
- Python 3.12+
- Google Gemini 3.6 Flash
- google-genai
- Pydantic
- Pandas
- python-dotenv
- Streamlit
- Pytest
- CSV
- JSON

SUPPORTED CATEGORIES AND ROUTING:

Authentication → Identity & Access Team
Payment → Payments Team
Technical Issue → Technical Support Team
Account → Account Management Team
Service Outage → Infrastructure Team
Shipping → Logistics Team
General → Customer Support Team

URGENCY LEVELS:
Critical:
Complete service outage, major production failure, security-related emergency, or issue affecting many users.

High:
Important functionality is blocked, payment problems are preventing an important transaction, or urgent assistance is needed.

Medium:
Normal customer support issue that affects the customer but is not immediately business-critical.

Low:
General questions, information requests, minor issues, or non-urgent requests.

HUMAN REVIEW:
The application uses a confidence threshold of 0.70.

confidence < 0.70 → human_review = True
confidence >= 0.70 → human_review = False

Exactly 0.70 does NOT require human review.

Explain that the confidence score is model-generated and is not statistically calibrated. With more labeled production data, the threshold could be tuned based on accuracy and business impact.

AI ARCHITECTURE:
The LLM determines the semantic category and urgency. The application then uses a deterministic routing map to determine the final support team.

Flow:
Support Ticket
→ Gemini AI
→ Category + Urgency + Confidence + Reason
→ Application Routing Map
→ Support Team
→ Human Review Decision
→ CSV/JSON Output

IMPORTANT IMPLEMENTATION DETAILS:

1. src/agent.py
- Loads GEMINI_API_KEY from .env
- Uses Gemini 3.6 Flash
- Uses structured JSON output validated with Pydantic
- Calls get_team() to determine routing
- Sets human_review based on confidence < 0.70
- Saves successful results to local cache
- Reads cached results before making a Gemini request
- Handles temporary 503/UNAVAILABLE errors using exponential backoff
- Handles 504/DEADLINE_EXCEEDED timeout errors with retries
- Handles 429/RESOURCE_EXHAUSTED without repeatedly retrying
- Gemini client timeout is configured to 120000 milliseconds

2. src/models.py
Defines a Pydantic TicketAnalysis model with:
- category
- urgency
- confidence
- route_to
- human_review
- reason

3. src/router.py
Contains deterministic category-to-team routing.

4. src/cache.py
Uses:
outputs/triage_cache.json

The cache key is based on a SHA-256 hash of ticket subject + message. Repeated identical tickets can be served from cache without another Gemini API call.

5. src/main.py
Supports:
python -m src.main

for real Gemini-powered batch processing.

Also supports:
python -m src.main --demo

for an offline deterministic demo that does NOT call Gemini.

6. app.py
Provides a Streamlit web interface with:
- Single ticket analysis
- Ticket subject and message input
- Gemini analysis
- Category display
- Urgency display
- Confidence score
- Confidence progress bar
- Routing team
- Human-review status
- AI reasoning
- Structured JSON output
- Batch CSV upload
- Batch processing
- Processing summary
- CSV download

SAMPLE INPUT:
Subject:
Payment failed

Message:
My card payment was declined twice and I need to complete the transaction today.

EXPECTED RESULT:
Category: Payment
Urgency: High
Confidence: 0.95 approximately
Route: Payments Team
Human Review: False

Example structured result:
{
  "category": "Payment",
  "urgency": "High",
  "confidence": 0.95,
  "route_to": "Payments Team",
  "human_review": false,
  "reason": "Customer experienced multiple payment declines for a transaction that needs to be completed today."
}

SAMPLE DATA:
data/sample_tickets.csv contains 15 support tickets covering the supported categories and urgency levels.

Verified offline demo result:
Processed tickets: 15

Categories:
Payment: 4
Authentication: 3
Service Outage: 2
Shipping: 2
Technical Issue: 2
Account: 1
General: 1

Urgency:
High: 6
Medium: 5
Critical: 2
Low: 2

Human Review:
False: 14
True: 1

TESTING:
The project currently has 10 automated tests and all 10 pass.

Command:
python -m pytest -v

Verified result:
10 passed

The tests cover:
- Payment routing
- Authentication routing
- Service Outage routing
- Shipping routing
- Technical Issue routing
- Account routing
- General routing
- High-confidence review decision
- Low-confidence review decision
- Exact 0.70 confidence boundary

REAL GEMINI TEST:
A real Gemini test was successfully performed using:
python -c "from src.agent import analyze_ticket; r=analyze_ticket('Payment failed','My card payment was declined twice and I need to complete the transaction today.'); print(r.model_dump())"

It successfully returned:
Payment
High
0.95
Payments Team
False

The first successful test also demonstrated retry handling after temporary Gemini 503 errors.

Running the same command again returned:
✓ Using cached result

This demonstrated that the local cache works and avoids another Gemini API request for the same ticket.

README MUST INCLUDE THESE SECTIONS:

1. Project title
2. Project overview
3. Problem statement
4. Solution
5. Key features
6. Architecture / workflow
7. Supported categories
8. Routing map
9. Urgency levels
10. Human-review decision boundary
11. How the AI agent works
12. Project structure
13. Technologies used
14. Requirements/prerequisites
15. Installation
16. Virtual environment setup for Windows and macOS/Linux
17. Dependency installation
18. Gemini API key setup
19. .env and .env.example instructions
20. Security warning about API keys
21. Running the Streamlit UI
22. Running the real Gemini CLI mode
23. Running the offline demo mode
24. Sample input
25. Sample output
26. Batch CSV input format
27. Batch output format
28. Caching explanation
29. Retry/error handling
30. Testing
31. Verified test results
32. Design decisions
33. Tradeoffs
34. Limitations
35. Future improvements
36. Agent-specific deliverables
37. Challenge requirements checklist
38. Quick-start section for reviewers
39. Demo instructions
40. Author section

INSTALLATION SHOULD INCLUDE EXACT COMMANDS:

Windows:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

macOS/Linux:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

ENV:
Create .env:
GEMINI_API_KEY=your_gemini_api_key_here

Never put a real key in README.

RUN COMMANDS:

Run tests:
python -m pytest -v

Offline demo:
python -m src.main --demo

Real Gemini batch processing:
python -m src.main

Streamlit:
streamlit run app.py

Explain that:
- --demo does NOT call Gemini
- Without --demo, the batch pipeline uses Gemini
- Streamlit uses the real analyze_ticket() function
- Repeated identical tickets can use the local cache

TRADEOFFS MUST DISCUSS:
1. Gemini LLM vs rule-based classification
2. Deterministic routing vs asking the LLM to choose teams
3. 0.70 confidence threshold
4. Local JSON cache vs production database
5. Streamlit UI vs production frontend
6. API dependency and quota
7. Model-generated confidence limitations

LIMITATIONS MUST BE HONEST:
- LLM classification can be wrong
- Confidence is not calibrated
- Static routing map
- Local JSON cache is not suitable for distributed production
- No authentication/user management
- No real helpdesk integration
- Human review is currently represented as a flag, not a real queue
- Gemini API availability and quota affect AI mode
- Batch AI processing consumes API quota

FUTURE IMPROVEMENTS:
- Zendesk/Freshdesk/Jira integration
- Database
- Confidence calibration
- Agent feedback loop
- Workload-aware routing
- SLA-aware prioritization
- Analytics dashboard
- Authentication
- Production monitoring
- Audit logs

CHALLENGE CHECKLIST SHOULD CLEARLY SHOW:
- Public GitHub repository → placeholder for URL
- README → completed
- Runnable agent → completed
- Sample inputs → data/sample_tickets.csv
- Sample outputs → outputs/triaged_tickets.csv
- Tradeoff notes → included
- Support ticket triage capabilities → included
- Classified/routed output → included
- Decision boundary explanation → included
- UI → optional but included

IMPORTANT:
Do not claim features that are not listed above.
Do not invent additional agents, databases, integrations, or capabilities.
Do not say the system is production-ready.
Describe it as a challenge/demo prototype.
Keep the README professional and evaluator-friendly.
Make setup instructions easy enough that a reviewer can run the project in a few minutes.
Use Markdown headings, tables, code blocks, and clear formatting.
Include an end-to-end example showing a ticket flowing from input through Gemini, classification, routing, human-review decision, and final output.
Leave a clear placeholder for the GitHub repository URL.
Return ONLY the complete README.md content, starting with "# 🎫 AI Support Ticket Triage Agent".
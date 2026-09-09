import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# Project import setup
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.agent import analyze_ticket


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Support Ticket Triage",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# Custom styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* Main page */
    .main {
        padding-top: 1rem;
    }

    /* Header */
    .hero {
        padding: 2rem 2.2rem;
        border-radius: 16px;
        background: linear-gradient(
            135deg,
            #111827,
            #1e293b
        );
        border: 1px solid #334155;
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
        color: #f8fafc;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #cbd5e1;
        margin: 0;
    }

    /* Section titles */
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    /* Result cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.2rem;
        min-height: 115px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    }

    .metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        font-size: 1.35rem;
        font-weight: 800;
        color: #0f172a;
    }

    /* Review boxes */
    .review-success {
        background: #ecfdf5;
        border: 1px solid #86efac;
        color: #166534;
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
    }

    .review-warning {
        background: #fff7ed;
        border: 1px solid #fdba74;
        color: #9a3412;
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
    }

    /* Info cards */
    .info-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
    }

    /* Analyze button */
    div.stButton > button[kind="primary"] {
        width: 100%;
        border-radius: 10px;
        min-height: 3rem;
        font-size: 1rem;
        font-weight: 700;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid #334155;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.8rem;
        padding: 1rem 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">
            🎫 AI Support Ticket Triage Agent
        </div>
        <p class="hero-subtitle">
            Automatically classify, prioritize, route, and flag
            customer support tickets using Gemini AI.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.markdown("## ⚙️ System")

    st.success("🟢 Gemini AI Connected")

    st.markdown("---")

    st.markdown("### 📂 Supported Categories")

    category_list = [
        "Authentication",
        "Payment",
        "Technical Issue",
        "Account",
        "Service Outage",
        "Shipping",
        "General",
    ]

    for category in category_list:
        st.write(f"• {category}")

    st.markdown("---")

    st.markdown("### 🎯 Decision Boundary")

    st.info(
        "Tickets with confidence below **70%** "
        "are automatically flagged for human review."
    )

    st.markdown("---")

    st.markdown("### 🤖 AI Model")

    st.write("Gemini 3.6 Flash")

    st.markdown("---")

    st.caption("Human-in-the-loop support triage")
    st.caption("Powered by Gemini")


# ---------------------------------------------------------
# Tabs
# ---------------------------------------------------------

single_tab, batch_tab = st.tabs(
    ["🎯 Single Ticket", "📊 Batch Processing"]
)


# =========================================================
# SINGLE TICKET
# =========================================================

with single_tab:

    st.markdown(
        '<div class="section-title">Analyze a Support Ticket</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 1])

    with col1:

        subject = st.text_input(
            "Ticket Subject",
            placeholder="Example: Payment failed",
        )

    with col2:

        st.markdown("#### ")

        st.caption(
            "Gemini analyzes the subject and message "
            "to determine the correct routing."
        )

    message = st.text_area(
        "Ticket Message",
        height=170,
        placeholder=(
            "Describe the customer's issue...\n\n"
            "Example:\n"
            "My card payment was declined twice and "
            "I need to complete the transaction today."
        ),
    )

    st.markdown("")

    analyze_button = st.button(
        "🔍  Analyze Ticket",
        type="primary",
        use_container_width=True,
    )

    # -----------------------------------------------------
    # Analysis
    # -----------------------------------------------------

    if analyze_button:

        if not subject.strip():

            st.warning(
                "Please enter a ticket subject."
            )

        elif not message.strip():

            st.warning(
                "Please enter the ticket message."
            )

        else:

            with st.spinner(
                "🤖 Gemini is analyzing the support ticket..."
            ):

                try:

                    result = analyze_ticket(
                        subject.strip(),
                        message.strip(),
                    )

                    st.success(
                        "Ticket analyzed successfully."
                    )

                    # -----------------------------------------
                    # Triage Decision
                    # -----------------------------------------

                    st.markdown(
                        '<div class="section-title">📋 Triage Decision</div>',
                        unsafe_allow_html=True,
                    )

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:

                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-label">
                                    Category
                                </div>
                                <div class="metric-value">
                                    {result.category}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with col2:

                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-label">
                                    Urgency
                                </div>
                                <div class="metric-value">
                                    {result.urgency}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with col3:

                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-label">
                                    Confidence
                                </div>
                                <div class="metric-value">
                                    {result.confidence:.0%}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with col4:

                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-label">
                                    Routed To
                                </div>
                                <div class="metric-value">
                                    {result.route_to}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    # -----------------------------------------
                    # Confidence
                    # -----------------------------------------

                    st.markdown(
                        '<div class="section-title">📊 Confidence Score</div>',
                        unsafe_allow_html=True,
                    )

                    st.progress(
                        min(
                            max(
                                result.confidence,
                                0.0,
                            ),
                            1.0,
                        )
                    )

                    st.caption(
                        f"AI confidence: "
                        f"**{result.confidence:.0%}** "
                        f"• Human-review threshold: **70%**"
                    )

                    # -----------------------------------------
                    # Human Review
                    # -----------------------------------------

                    if result.human_review:

                        st.markdown(
                            """
                            <div class="review-warning">
                                <strong>
                                    ⚠️ Human Review Required
                                </strong>
                                <br>
                                The model confidence is below
                                the 70% decision boundary.
                                A human should review this ticket
                                before final routing.
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    else:

                        st.markdown(
                            """
                            <div class="review-success">
                                <strong>
                                    ✅ No Human Review Required
                                </strong>
                                <br>
                                The model confidence meets the
                                70% decision boundary.
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    # -----------------------------------------
                    # AI reasoning
                    # -----------------------------------------

                    st.markdown(
                        '<div class="section-title">💡 AI Reasoning</div>',
                        unsafe_allow_html=True,
                    )

                    st.info(result.reason)

                    # -----------------------------------------
                    # Structured output
                    # -----------------------------------------

                    with st.expander(
                        "🔎 View Structured JSON Output"
                    ):

                        structured_output = {
                            "category": result.category,
                            "urgency": result.urgency,
                            "confidence": result.confidence,
                            "route_to": result.route_to,
                            "human_review": result.human_review,
                            "reason": result.reason,
                        }

                        st.json(
                            structured_output
                        )

                except Exception as e:

                    st.error(
                        "Unable to analyze the ticket."
                    )

                    with st.expander(
                        "Technical Details"
                    ):

                        st.code(
                            str(e)
                        )


# =========================================================
# BATCH PROCESSING
# =========================================================

with batch_tab:

    st.markdown(
        '<div class="section-title">📊 Batch Ticket Processing</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Upload a CSV containing multiple support tickets. "
        "Each ticket will be classified, prioritized, routed, "
        "and evaluated for human review."
    )

    st.info(
        "Required CSV columns: "
        "**ticket_id**, **subject**, **message**"
    )

    uploaded_file = st.file_uploader(
        "📤 Upload Support Ticket CSV",
        type=["csv"],
    )

    if uploaded_file is not None:

        try:

            df = pd.read_csv(
                uploaded_file
            )

            required_columns = {
                "ticket_id",
                "subject",
                "message",
            }

            missing_columns = (
                required_columns
                - set(df.columns)
            )

            if missing_columns:

                st.error(
                    "Missing required columns: "
                    + ", ".join(
                        sorted(
                            missing_columns
                        )
                    )
                )

            else:

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Tickets Uploaded",
                        len(df),
                    )

                with col2:

                    st.metric(
                        "Required Columns",
                        "3 / 3",
                    )

                with col3:

                    st.metric(
                        "Processing Mode",
                        "Gemini AI",
                    )

                st.markdown(
                    "### 📄 Input Preview"
                )

                st.dataframe(
                    df.head(10),
                    use_container_width=True,
                )

                st.markdown("")

                process_button = st.button(
                    "🚀 Process All Tickets",
                    type="primary",
                    use_container_width=True,
                )

                if process_button:

                    results = []

                    progress = st.progress(
                        0
                    )

                    status = st.empty()

                    for index, row in df.iterrows():

                        ticket_id = str(
                            row["ticket_id"]
                        )

                        status.write(
                            f"🤖 Processing **{ticket_id}**..."
                        )

                        try:

                            result = analyze_ticket(
                                str(
                                    row["subject"]
                                ),
                                str(
                                    row["message"]
                                ),
                            )

                            results.append(
                                {
                                    "ticket_id": ticket_id,
                                    "subject": row["subject"],
                                    "category": result.category,
                                    "urgency": result.urgency,
                                    "confidence": result.confidence,
                                    "route_to": result.route_to,
                                    "human_review": result.human_review,
                                    "processing_status": "CLASSIFIED",
                                    "reason": result.reason,
                                }
                            )

                        except Exception:

                            results.append(
                                {
                                    "ticket_id": ticket_id,
                                    "subject": row["subject"],
                                    "category": "",
                                    "urgency": "",
                                    "confidence": "",
                                    "route_to": "",
                                    "human_review": "",
                                    "processing_status": "API_ERROR",
                                    "reason": "Ticket could not be processed.",
                                }
                            )

                        progress.progress(
                            (index + 1)
                            / len(df)
                        )

                    status.success(
                        "✅ All tickets processed successfully."
                    )

                    result_df = pd.DataFrame(
                        results
                    )

                    st.markdown(
                        "### 📋 Triage Results"
                    )

                    st.dataframe(
                        result_df,
                        use_container_width=True,
                    )

                    # -----------------------------------------
                    # Batch summary
                    # -----------------------------------------

                    st.markdown(
                        "### 📈 Processing Summary"
                    )

                    total = len(
                        result_df
                    )

                    review_count = (
                        result_df[
                            "human_review"
                        ]
                        .astype(str)
                        .str.lower()
                        .eq("true")
                        .sum()
                    )

                    classified_count = (
                        result_df[
                            "processing_status"
                        ]
                        .eq("CLASSIFIED")
                        .sum()
                    )

                    average_confidence = pd.to_numeric(
                        result_df[
                            "confidence"
                        ],
                        errors="coerce",
                    ).mean()

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:

                        st.metric(
                            "Tickets",
                            total,
                        )

                    with col2:

                        st.metric(
                            "Classified",
                            int(
                                classified_count
                            ),
                        )

                    with col3:

                        st.metric(
                            "Human Review",
                            int(
                                review_count
                            ),
                        )

                    with col4:

                        if pd.notna(
                            average_confidence
                        ):

                            st.metric(
                                "Avg. Confidence",
                                f"{average_confidence:.0%}",
                            )

                        else:

                            st.metric(
                                "Avg. Confidence",
                                "N/A",
                            )

                    # -----------------------------------------
                    # Download
                    # -----------------------------------------

                    csv_data = (
                        result_df
                        .to_csv(
                            index=False
                        )
                        .encode(
                            "utf-8"
                        )
                    )

                    st.download_button(
                        "📥 Download Triaged Tickets CSV",
                        data=csv_data,
                        file_name="triaged_tickets.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )

        except Exception as e:

            st.error(
                f"Could not read the CSV file: {e}"
            )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        AI Support Ticket Triage Agent
        &nbsp;•&nbsp;
        Gemini-powered
        &nbsp;•&nbsp;
        Human-in-the-loop design
    </div>
    """,
    unsafe_allow_html=True,
)
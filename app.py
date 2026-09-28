import os
import re
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight


# ============================================================
# CONFIG
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

HINDSIGHT_URL = "http://localhost:8890"
BANK_ID = "fieldmind"
MODEL = "openai/gpt-oss-20b"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FieldMind",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# SIMPLE CSS
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero-text {
        color: #9aa4bd;
        font-size: 17px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CLIENTS
# ============================================================

if not GROQ_API_KEY:
    st.error(
        "GROQ_API_KEY is missing. Check your .env file."
    )
    st.stop()


groq_client = Groq(
    api_key=GROQ_API_KEY
)

memory_client = Hindsight(
    base_url=HINDSIGHT_URL
)


# ============================================================
# SESSION STATE
# ============================================================

if "memories" not in st.session_state:
    st.session_state.memories = []

if "analysis" not in st.session_state:
    st.session_state.analysis = ""

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🧠 FieldMind")

    st.caption(
        "Every incident teaches the next one."
    )

    st.divider()

    st.success(
        "Hindsight Connected"
    )

    st.subheader(
        "Operational Memory"
    )

    st.write(
        "🧠 Remembers incidents"
    )

    st.write(
        "🔎 Recalls similar cases"
    )

    st.write(
        "🔗 Detects patterns"
    )

    st.write(
        "📚 Learns from outcomes"
    )

    st.write(
        "💡 Supports better decisions"
    )

    st.divider()

    st.caption(
        "Powered by Hindsight + Groq"
    )


# ============================================================
# HERO
# ============================================================

st.title("🧠 FieldMind")

st.subheader(
    "Every incident teaches the next one."
)

st.markdown(
    """
    <div class="hero-text">
    FieldMind is an AI operational-memory agent that remembers
    what happened, learns what worked and failed, and helps
    field teams solve the next incident faster.
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# METRICS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Long-term Memory",
        "∞"
    )

with c2:
    st.metric(
        "Historical Recall",
        "ON"
    )

with c3:
    st.metric(
        "Pattern Learning",
        "AI"
    )

with c4:
    st.metric(
        "Decision Support",
        "⚡"
    )


st.divider()


# ============================================================
# INCIDENT INPUT
# ============================================================

st.header(
    "🔍 Analyze a Field Incident"
)

st.write(
    "Describe an incident and let FieldMind use "
    "organizational memory to guide the next decision."
)


left, right = st.columns(2)


with left:

    location = st.text_input(
        "📍 Location",
        placeholder="Lakshmi Nagar Water Station"
    )

    incident_type = st.selectbox(
        "⚠️ Incident Type",
        [
            "Pump Failure",
            "Low Water Pressure",
            "Transformer Overheating",
            "Transformer Alarm",
            "Streetlight Outage",
            "Pressure Drop",
            "Other"
        ]
    )


with right:

    severity = st.selectbox(
        "🚨 Severity",
        [
            "Low",
            "Medium",
            "High",
            "Critical"
        ]
    )

    description = st.text_area(
        "📝 Incident Description",
        placeholder=(
            "Describe what happened, what was observed, "
            "and what was tried previously..."
        ),
        height=140
    )


analyze = st.button(
    "🔍 Analyze With FieldMind",
    type="primary",
    use_container_width=True
)


# ============================================================
# ANALYZE
# ============================================================

if analyze:

  location_clean = location.strip()

if not location_clean:
    st.warning("Please enter the incident location.")
    st.stop()

if re.search(r"[\w\.-]+@[\w\.-]+\.\w+", location_clean):
    st.error(
        "❌ Please enter a field location, not an email address."
    )
    st.stop()

    if not description.strip():

        st.warning(
            "Please describe the incident."
        )

        st.stop()


    # --------------------------------------------------------
    # INCIDENT
    # --------------------------------------------------------

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )

    incident = f"""
Field Incident

Date: {timestamp}
Location: {location}
Incident Type: {incident_type}
Severity: {severity}

Description:
{description}
""".strip()


    # --------------------------------------------------------
    # HINDSIGHT RETAIN
    # --------------------------------------------------------

    with st.spinner(
        "🧠 Storing incident in organizational memory..."
    ):

        try:

            memory_client.retain(
                bank_id=BANK_ID,
                content=incident,
                context="field operations incident"
            )

        except Exception as e:

            st.error(
                f"Hindsight retain error: {e}"
            )

            st.stop()


    # --------------------------------------------------------
    # HINDSIGHT RECALL
    # --------------------------------------------------------

    recall_query = f"""
Find the most relevant historical field incidents
for the current problem.

Current location:
{location}

Current incident type:
{incident_type}

Current severity:
{severity}

Current description:
{description}

Prioritize memories that contain:
1. Similar incidents
2. Root causes
3. Actions taken
4. What worked
5. What failed
6. Long-term outcomes
7. Lessons learned

Return the most useful memories for making the next decision.
"""


    with st.spinner(
        "🔎 Searching organizational memory..."
    ):

        try:

            recall_response = memory_client.recall(
                bank_id=BANK_ID,
                query=recall_query
            )

            memories = getattr(
                recall_response,
                "results",
                []
            )

            # Only use the top 6 for the AI.
            # This keeps the reasoning focused.
            memories = memories[:6]

            st.session_state.memories = memories

        except Exception as e:

            st.error(
                f"Hindsight recall error: {e}"
            )

            st.stop()


    # --------------------------------------------------------
    # FORMAT MEMORY
    # --------------------------------------------------------

    if memories:

        memory_text = ""

        for i, memory in enumerate(
            memories,
            start=1
        ):

            memory_content = getattr(
                memory,
                "text",
                str(memory)
            )

            memory_text += f"""
MEMORY {i}
{memory_content}

"""


    else:

        memory_text = (
            "No relevant historical memories were found."
        )


    # --------------------------------------------------------
    # GROQ PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are FieldMind, an AI operational-memory agent.

Your unique job is to use organizational memory
to improve decisions for recurring field incidents.

Do NOT give a generic troubleshooting answer.

CURRENT INCIDENT
================

Location:
{location}

Incident Type:
{incident_type}

Severity:
{severity}

Description:
{description}


HISTORICAL ORGANIZATIONAL MEMORY
================================

{memory_text}


TASK
====

Analyze the current incident using the historical memories.

Your response MUST contain these six headings:

1. PATTERN
2. HISTORICAL EVIDENCE
3. WHAT WORKED
4. WHAT FAILED
5. RECOMMENDATION
6. WHY THIS RECOMMENDATION

For RECOMMENDATION:

Give a practical action that the field team
should take next.

For WHY THIS RECOMMENDATION:

Explicitly explain how the historical evidence
supports your recommendation.

Very important:

Do not invent historical events.

If a previous intervention failed,
say that it failed.

If another intervention worked better,
explain that difference.

Keep the response concise enough for a field operator.
"""


    # --------------------------------------------------------
    # GROQ
    # --------------------------------------------------------

    with st.spinner(
        "🤖 Learning from previous incidents..."
    ):

        try:

            response = groq_client.chat.completions.create(

                model=MODEL,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are FieldMind. "
                            "You reason using retrieved "
                            "organizational memory."
                        )
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.1,

                max_tokens=1400
            )


            analysis = (
                response
                .choices[0]
                .message
                .content
            )


            # SAVE COMPLETE AI RESPONSE
            st.session_state.analysis = analysis

            st.session_state.analyzed = True


        except Exception as e:

            st.error(
                f"Groq analysis error: {e}"
            )

            st.stop()


# ============================================================
# RESULTS
# ============================================================

if st.session_state.analyzed:

    memories = st.session_state.memories

    analysis = st.session_state.analysis


    st.divider()


    # ========================================================
    # MEMORY JOURNEY
    # ========================================================

    st.header(
        "🧠 FieldMind Memory Journey"
    )

    st.caption(
        "How organizational memory changes the next decision."
    )


    j1, j2, j3, j4 = st.columns(4)


    with j1:

        st.subheader(
            "01"
        )

        st.write(
            "📋 Current Incident"
        )

        st.caption(
            "The new incident is captured."
        )


    with j2:

        st.subheader(
            "02"
        )

        st.write(
            "🔎 Historical Memory"
        )

        st.caption(
            "Hindsight recalls similar cases."
        )


    with j3:

        st.subheader(
            "03"
        )

        st.write(
            "🔗 Pattern Detected"
        )

        st.caption(
            "Past outcomes reveal lessons."
        )


    with j4:

        st.subheader(
            "04"
        )

        st.write(
            "💡 Better Decision"
        )

        st.caption(
            "The next action uses experience."
        )


    st.divider()


    # ========================================================
    # IMPORTANT: SHOW COMPLETE AI RESPONSE
    # ========================================================

    st.header(
        "🤖 FieldMind Decision Analysis"
    )

    # This guarantees that the AI response is visible.
    st.write(
        analysis
    )


    st.divider()


    # ========================================================
    # RECOMMENDATION HIGHLIGHT
    # ========================================================

    recommendation = ""

    why = ""

    pattern = ""

    historical = ""

    worked = ""

    failed = ""


    # Try to extract sections
    current = None

    sections = {
        "PATTERN": [],
        "HISTORICAL EVIDENCE": [],
        "WHAT WORKED": [],
        "WHAT FAILED": [],
        "RECOMMENDATION": [],
        "WHY THIS RECOMMENDATION": []
    }


    for line in analysis.splitlines():

        line_clean = line.strip()

        upper = line_clean.upper()


        if upper.startswith("PATTERN:"):

            current = "PATTERN"

            sections[current].append(
                line_clean.split(
                    ":",
                    1
                )[1].strip()
            )

            continue


        if upper.startswith("HISTORICAL EVIDENCE:"):

            current = "HISTORICAL EVIDENCE"

            sections[current].append(
                line_clean.split(
                    ":",
                    1
                )[1].strip()
            )

            continue


        if upper.startswith("WHAT WORKED:"):

            current = "WHAT WORKED"

            sections[current].append(
                line_clean.split(
                    ":",
                    1
                )[1].strip()
            )

            continue


        if upper.startswith("WHAT FAILED:"):

            current = "WHAT FAILED"

            sections[current].append(
                line_clean.split(
                    ":",
                    1
                )[1].strip()
            )

            continue


        if upper.startswith("RECOMMENDATION:"):

            current = "RECOMMENDATION"

            sections[current].append(
                line_clean.split(
                    ":",
                    1
                )[1].strip()
            )

            continue


        if upper.startswith(
            "WHY THIS RECOMMENDATION:"
        ):

            current = "WHY THIS RECOMMENDATION"

            sections[current].append(
                line_clean.split(
                    ":",
                    1
                )[1].strip()
            )

            continue


        if current and line_clean:

            sections[current].append(
                line_clean
            )


    pattern = " ".join(
        sections["PATTERN"]
    ).strip()

    historical = " ".join(
        sections["HISTORICAL EVIDENCE"]
    ).strip()

    worked = " ".join(
        sections["WHAT WORKED"]
    ).strip()

    failed = " ".join(
        sections["WHAT FAILED"]
    ).strip()

    recommendation = " ".join(
        sections["RECOMMENDATION"]
    ).strip()

    why = " ".join(
        sections["WHY THIS RECOMMENDATION"]
    ).strip()


    # ========================================================
    # SHOW RECOMMENDATION
    # ========================================================

    if recommendation:

        st.subheader(
            "💡 Recommended Next Action"
        )

        st.success(
            recommendation
        )

    else:

        st.subheader(
            "💡 Recommended Next Action"
        )

        st.warning(
            "The AI did not return a separately formatted "
            "recommendation. See the complete Decision Analysis "
            "above."
        )


    # ========================================================
    # WHY
    # ========================================================

    if why:

        st.subheader(
            "🧠 Why This Recommendation?"
        )

        st.info(
            why
        )


    # ========================================================
    # SUPPORTING EVIDENCE
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        if worked:

            st.subheader(
                "✅ What Worked"
            )

            st.success(
                worked
            )


    with col2:

        if failed:

            st.subheader(
                "❌ What Failed"
            )

            st.error(
                failed
            )


    if pattern:

        st.subheader(
            "🔁 Pattern Detected"
        )

        st.info(
            pattern
        )


    if historical:

        st.subheader(
            "📚 Historical Evidence"
        )

        st.write(
            historical
        )


    # ========================================================
    # MEMORY EVIDENCE
    # ========================================================

    st.divider()

    st.header(
        "📖 Memories Used"
    )

    st.caption(
        f"{len(memories)} relevant memories retrieved from Hindsight."
    )


    if memories:

        for i, memory in enumerate(
            memories,
            start=1
        ):

            memory_text = getattr(
                memory,
                "text",
                str(memory)
            )

            with st.expander(
                f"Memory {i}"
            ):

                st.write(
                    memory_text
                )

    else:

        st.info(
            "No relevant historical memories were found."
        )


    # ========================================================
    # SUCCESS
    # ========================================================

    st.success(
        "🧠 Memory updated — this incident can now influence future decisions."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "FieldMind · Every incident teaches the next one. "
    "Persistent operational memory powered by Hindsight."
)